import json
import time
from datetime import datetime
import statistics

class ProcesadorLambda:
    def procesar_batch(self, archivo_entrada):
        """Procesamiento BATCH (lento pero completo) - LAMBDA"""
        print(" Procesando BATCH (Lambda Architecture)...")
        time.sleep(3)  # Simula procesamiento lento
        
        try:
            with open(archivo_entrada, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
                datos = [json.loads(linea) for linea in lineas]
            
            if not datos:
                return {"error": "No hay datos"}
            
            # Análisis completo
            temperaturas = [d['temperatura'] for d in datos]
            dispositivos = list(set(d['dispositivo'] for d in datos))
            
            resultado = {
                "arquitectura": "LAMBDA - BATCH",
                "total_datos": len(datos),
                "temperatura_promedio": round(statistics.mean(temperaturas), 2),
                "temperatura_maxima": round(max(temperaturas), 2),
                "temperatura_minima": round(min(temperaturas), 2),
                "dispositivos_unicos": len(dispositivos),
                "tiempo_procesamiento": "3 segundos (simulado)",
                "timestamp": datetime.now().isoformat()
            }
            
            print(" Procesamiento BATCH completado")
            return resultado
            
        except Exception as e:
            return {"error": f"Error en batch: {str(e)}"}
    
    def procesar_realtime(self, archivo_entrada):
        """Procesamiento REAL-TIME (rápido) - LAMBDA"""
        print("⚡ Procesando REAL-TIME (Lambda Architecture)...")
        time.sleep(1)  # Simula procesamiento rápido
        
        try:
            with open(archivo_entrada, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
                if not lineas:
                    return {"error": "No hay datos"}
                
                ultimo_dato = json.loads(lineas[-1])
            
            resultado = {
                "arquitectura": "LAMBDA - REAL-TIME", 
                "ultimo_dato": ultimo_dato,
                "total_datos": len(lineas),
                "tiempo_procesamiento": "1 segundo (simulado)",
                "timestamp": datetime.now().isoformat()
            }
            
            print(" Procesamiento REAL-TIME completado")
            return resultado
            
        except Exception as e:
            return {"error": f"Error en real-time: {str(e)}"}

# Prueba individual
if __name__ == "__main__":
    procesador = ProcesadorLambda()
    
    print(" Probando Lambda Architecture:")
    print("1. Procesamiento BATCH (lento):")
    resultado_batch = procesador.procesar_batch("datos_batch.json")
    print(json.dumps(resultado_batch, indent=2))
    
    print("\n2. Procesamiento REAL-TIME (rápido):")
    resultado_realtime = procesador.procesar_realtime("datos_realtime.json")
    print(json.dumps(resultado_realtime, indent=2))