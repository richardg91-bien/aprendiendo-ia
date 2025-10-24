#!/usr/bin/env python3
"""
📚 CARGADOR MASIVO DE CONOCIMIENTO PARA ARIA
===========================================

Script para cargar toda la base de conocimiento expandida a Supabase
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from dotenv import load_dotenv
load_dotenv()

from aria_enhanced_connector import get_enhanced_connector

def load_knowledge_base():
    """Cargar toda la base de conocimiento a Supabase"""
    
    # Base de conocimiento expandida (misma que en el servidor)
    knowledge_base = {
        # === EMOCIONES Y SENTIMIENTOS ===
        'amor': "El amor es un sentimiento profundo de afecto, cariño y conexión hacia otra persona, objeto o idea. Incluye aspectos emocionales, físicos y espirituales, manifestándose en diferentes formas como amor romántico, familiar, platónico y universal. Es considerado una de las experiencias humanas más fundamentales.",
        'felicidad': "La felicidad es un estado emocional caracterizado por sentimientos de alegría, satisfacción, plenitud y realización. Es considerada uno de los objetivos fundamentales de la vida humana y puede ser influenciada por factores internos y externos.",
        'tristeza': "La tristeza es una emoción humana básica que surge como respuesta a pérdidas, desilusiones o situaciones dolorosas. Aunque puede ser incómoda, es natural y necesaria para el procesamiento emocional y la adaptación.",
        'miedo': "El miedo es una emoción básica de supervivencia que nos alerta ante peligros reales o percibidos. Puede ser adaptativo cuando nos protege, pero limitante cuando es excesivo o irracional.",
        'ira': "La ira es una emoción intensa que surge ante la percepción de injusticia, frustración o amenaza. Puede ser constructiva si se canaliza adecuadamente, pero destructiva si no se gestiona bien.",
        'amistad': "La amistad es una relación afectiva entre personas basada en el respeto mutuo, la confianza, el apoyo emocional y el compartir experiencias. Es fundamental para el bienestar social y emocional humano.",
        'soledad': "La soledad es la experiencia subjetiva de aislamiento o desconexión social. Puede ser elegida (solitud) o no deseada, y tiene impactos significativos en la salud mental y física.",
        'esperanza': "La esperanza es un estado emocional positivo basado en la expectativa de que eventos favorables ocurrirán en el futuro. Es fundamental para la motivación y la resiliencia humana.",
        
        # === CONCEPTOS FILOSÓFICOS ===
        'vida': "La vida es el estado de actividad continua propio de los seres orgánicos, caracterizada por el crecimiento, la reproducción, el metabolismo y la capacidad de respuesta al entorno. Filosóficamente, se considera el bien más preciado.",
        'muerte': "La muerte es el final de la vida, el cese permanente de todas las funciones vitales. Es un fenómeno natural que ha generado reflexiones filosóficas, religiosas y científicas a lo largo de la historia humana.",
        'existencia': "La existencia es el hecho de ser, de tener realidad. En filosofía, se estudia como el estado de ser algo real en contraposición a la no-existencia o la mera posibilidad.",
        'libertad': "La libertad es la capacidad de actuar según la propia voluntad, sin restricciones externas indebidas. Incluye aspectos políticos, sociales, morales y existenciales del ser humano.",
        'justicia': "La justicia es el principio moral que busca dar a cada uno lo que le corresponde, manteniendo el equilibrio entre derechos y deberes en la sociedad.",
        'verdad': "La verdad es la conformidad entre lo que se afirma y la realidad. Es un concepto central en filosofía, ciencia y vida cotidiana, buscada a través del conocimiento y la experiencia.",
        'belleza': "La belleza es una cualidad que produce placer estético, admiración o satisfacción. Puede encontrarse en objetos, personas, ideas o experiencias, y es tanto objetiva como subjetiva.",
        'sabiduría': "La sabiduría es la capacidad de usar el conocimiento y la experiencia para tomar decisiones acertadas y comprender la vida profundamente. Va más allá del mero conocimiento intelectual.",
        
        # === CIENCIA Y UNIVERSO ===
        'universo': "El universo es la totalidad del espacio-tiempo, toda la materia y energía que existe. Incluye planetas, estrellas, galaxias y toda la materia y energía conocida, así como las leyes físicas que las rigen.",
        'tiempo': "El tiempo es una magnitud física que permite ordenar la secuencia de eventos, estableciendo un pasado, presente y futuro. Es una dimensión fundamental en la que se desarrollan los procesos y cambios.",
        'espacio': "El espacio es la extensión tridimensional en la que se ubican y mueven los objetos. En física moderna, se entiende unificado con el tiempo como espacio-tiempo.",
        'gravedad': "La gravedad es la fuerza fundamental que atrae objetos con masa entre sí. Es responsable de la estructura del universo a gran escala y de fenómenos como las órbitas planetarias.",
        'evolución': "La evolución es el proceso de cambio y desarrollo de las especies a lo largo del tiempo, principalmente a través de la selección natural y otros mecanismos evolutivos.",
        'adn': "El ADN (ácido desoxirribonucleico) es la molécula que contiene las instrucciones genéticas para el desarrollo y funcionamiento de todos los seres vivos conocidos.",
        'energía': "La energía es la capacidad de realizar trabajo o producir cambios. Se manifiesta en diversas formas (cinética, potencial, térmica, etc.) y se conserva según las leyes físicas.",
        'átomo': "El átomo es la unidad básica de la materia, compuesto por un núcleo de protones y neutrones rodeado por electrones. Es la base de toda la química y la física de materiales.",
        
        # === MENTE Y CONSCIENCIA ===
        'consciencia': "La consciencia es la capacidad de ser consciente de uno mismo y del entorno, incluyendo pensamientos, sensaciones y experiencias. Es uno de los fenómenos más estudiados en neurociencia y filosofía.",
        'mente': "La mente es el conjunto de procesos cognitivos y emocionales que emergen del cerebro, incluyendo pensamientos, percepciones, emociones, memoria y consciencia.",
        'inteligencia': "La inteligencia es la capacidad de adquirir y aplicar conocimientos, resolver problemas, adaptarse a nuevas situaciones y comprender conceptos complejos.",
        'memoria': "La memoria es la capacidad de codificar, almacenar y recuperar información. Es fundamental para el aprendizaje, la identidad personal y la función cognitiva.",
        'creatividad': "La creatividad es la capacidad de generar ideas, soluciones o expresiones nuevas y valiosas. Combina imaginación, originalidad y utilidad práctica o estética.",
        'intuición': "La intuición es la capacidad de comprender o conocer algo de manera inmediata, sin necesidad de razonamiento consciente. Complementa el pensamiento analítico.",
        'personalidad': "La personalidad es el conjunto de características psicológicas duraderas que definen el patrón único de pensamientos, emociones y comportamientos de una persona.",
        
        # === TECNOLOGÍA E IA ===
        'inteligencia artificial': "La inteligencia artificial (IA) es la capacidad de las máquinas para realizar tareas que normalmente requieren inteligencia humana, como el aprendizaje, la percepción, el razonamiento y la toma de decisiones.",
        'machine learning': "El machine learning o aprendizaje automático es un subcampo de la IA que permite a los sistemas aprender y mejorar automáticamente a partir de datos sin ser programados explícitamente.",
        'deep learning': "El deep learning es una técnica de machine learning basada en redes neuronales artificiales profundas, capaz de aprender patrones complejos en grandes cantidades de datos.",
        'blockchain': "Blockchain es una tecnología de registro distribuido que mantiene una lista de registros (bloques) enlazados y asegurados usando criptografía, proporcionando transparencia y seguridad.",
        'internet': "Internet es una red global de computadoras interconectadas que permite el intercambio de información y comunicación a escala mundial, transformando la sociedad moderna.",
        'realidad virtual': "La realidad virtual es una tecnología que crea entornos simulados inmersivos, permitiendo a los usuarios interactuar con mundos digitales como si fueran reales.",
        'ciberseguridad': "La ciberseguridad es la práctica de proteger sistemas digitales, redes y datos de ataques, accesos no autorizados y daños maliciosos.",
        
        # === PROGRAMACIÓN ===
        'python': "Python es un lenguaje de programación de alto nivel, interpretado y de propósito general. Es conocido por su sintaxis clara y legible, lo que lo hace ideal para principiantes y profesionales.",
        'javascript': "JavaScript es un lenguaje de programación interpretado que se utiliza principalmente para crear páginas web dinámicas e interactivas y aplicaciones web modernas.",
        'html': "HTML (HyperText Markup Language) es el lenguaje de marcado estándar para crear páginas web, definiendo la estructura y el contenido de los documentos web.",
        'css': "CSS (Cascading Style Sheets) es un lenguaje de diseño utilizado para describir la presentación y el estilo visual de documentos HTML.",
        'programación': "La programación es el proceso de crear instrucciones para que las computadoras realicen tareas específicas, utilizando lenguajes de programación y algoritmos.",
        'algoritmo': "Un algoritmo es una secuencia de pasos lógicos y finitos diseñada para resolver un problema específico o realizar una tarea determinada.",
        
        # === SOCIEDAD Y CULTURA ===
        'educación': "La educación es el proceso de facilitar el aprendizaje y la adquisición de conocimientos, habilidades, valores y hábitos. Es fundamental para el desarrollo personal y social.",
        'cultura': "La cultura es el conjunto de conocimientos, creencias, arte, moral, leyes, costumbres y capacidades adquiridas por el ser humano como miembro de la sociedad.",
        'democracia': "La democracia es un sistema de gobierno en el que el poder reside en el pueblo, quien lo ejerce directamente o a través de representantes elegidos libremente.",
        'globalización': "La globalización es el proceso de integración económica, política, social y cultural a escala mundial, facilitado por avances en comunicación y transporte.",
        'sostenibilidad': "La sostenibilidad es la capacidad de satisfacer las necesidades actuales sin comprometer la capacidad de las futuras generaciones para satisfacer sus propias necesidades.",
        'diversidad': "La diversidad es la variedad y diferencia en características como cultura, raza, género, edad, religión y perspectivas, enriqueciendo la experiencia humana.",
        
        # === SALUD Y BIENESTAR ===
        'salud': "La salud es un estado de completo bienestar físico, mental y social, no solamente la ausencia de enfermedad, según la definición de la Organización Mundial de la Salud.",
        'ejercicio': "El ejercicio es la actividad física planificada y repetitiva diseñada para mejorar o mantener la condición física, la salud y el bienestar general.",
        'nutrición': "La nutrición es la ciencia que estudia los nutrientes y su relación con la salud, enfocándose en cómo los alimentos afectan el crecimiento, desarrollo y bienestar.",
        'meditación': "La meditación es una práctica mental que busca entrenar la atención y la consciencia para lograr claridad mental, estabilidad emocional y bienestar.",
        'estrés': "El estrés es la respuesta física y emocional del cuerpo ante situaciones desafiantes, que puede ser positivo en pequeñas dosis pero dañino cuando es crónico.",
        
        # === ARTE Y EXPRESIÓN ===
        'arte': "El arte es la expresión creativa humana que busca comunicar ideas, emociones o experiencias a través de diversos medios como pintura, música, literatura y escultura.",
        'música': "La música es el arte de organizar sonidos en el tiempo para crear expresiones estéticas y emocionales, utilizando elementos como ritmo, melodía y armonía.",
        'literatura': "La literatura es el arte de la expresión escrita, que utiliza el lenguaje de manera creativa para contar historias, expresar ideas y explorar la condición humana.",
        'poesía': "La poesía es una forma de expresión literaria que utiliza el lenguaje de manera intensificada y artística, a menudo con ritmo, métrica y simbolismo.",
        
        # === ECONOMÍA ===
        'economía': "La economía es la ciencia que estudia cómo las sociedades administran sus recursos escasos para satisfacer las necesidades y deseos humanos.",
        'dinero': "El dinero es un medio de intercambio, unidad de cuenta y depósito de valor que facilita las transacciones económicas en la sociedad.",
        'inflación': "La inflación es el aumento generalizado y sostenido de los precios de bienes y servicios en una economía durante un período determinado.",
        
        # === CONCEPTOS GENERALES ===
        'comunicación': "La comunicación es el proceso de intercambio de información, ideas, pensamientos y sentimientos entre individuos a través de diversos canales y medios.",
        'liderazgo': "El liderazgo es la capacidad de influir, motivar y dirigir a otros hacia el logro de objetivos comunes, combinando visión, habilidades sociales y toma de decisiones.",
        'innovación': "La innovación es el proceso de crear e implementar nuevas ideas, productos, servicios o procesos que generan valor y mejoras significativas.",
        'colaboración': "La colaboración es el trabajo conjunto de individuos o grupos hacia objetivos comunes, combinando habilidades, conocimientos y recursos para lograr mejores resultados."
    }
    
    print("📚 CARGANDO BASE DE CONOCIMIENTO EXPANDIDA A SUPABASE")
    print("=" * 60)
    
    # Conectar a Supabase
    connector = get_enhanced_connector()
    
    if not connector:
        print("❌ No se pudo conectar a Supabase")
        return False
    
    success_count = 0
    error_count = 0
    
    for concept, description in knowledge_base.items():
        try:
            print(f"📖 Cargando: {concept}")
            
            success = connector.store_knowledge(
                concept=concept,
                description=description,
                category="knowledge_base",
                confidence=0.9
            )
            
            if success:
                success_count += 1
                print(f"   ✅ Guardado correctamente")
            else:
                error_count += 1
                print(f"   ❌ Error al guardar")
                
        except Exception as e:
            error_count += 1
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESUMEN:")
    print(f"   ✅ Exitosos: {success_count}")
    print(f"   ❌ Errores: {error_count}")
    print(f"   📚 Total procesados: {len(knowledge_base)}")
    print(f"   📈 Tasa de éxito: {(success_count/len(knowledge_base)*100):.1f}%")
    
    return success_count > 0

if __name__ == "__main__":
    load_knowledge_base()