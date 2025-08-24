import json
import time
from datetime import datetime
import statistics

class ProcesadorKappa:
    def procesar_stream(self, archivo_entrada):
        """Procesamiento de STREAM (todo en tiempo real) - KAPPA"""
        print(" Procesando STREAM (Kappa Architecture)...")
        time.sleep(2)  # Simula procesamiento moderado
        
        try:
            with open(archivo_entrada, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
                datos = [json.loads(linea) for linea in lineas]
            
            if not datos:
                return {"error": "No hay datos"}
            
            # Análisis de stream (últimos datos)
            ultimos_datos = datos[-10:]  # Últimos 10 datos
            temperaturas = [d['temperatura'] for d in ultimos_datos]
            
            resultado = {
                "arquitectura": "KAPPA - STREAM",
                "total_datos": len(datos),
                "datos_recientes": len(ultimos_datos),
                "temperatura_promedio_reciente": round(statistics.mean(temperaturas), 2),
                "ultimo_dispositivo": ultimos_datos[-1]['dispositivo'] if ultimos_datos else "N/A",
                "ultima_temperatura": ultimos_datos[-1]['temperatura'] if ultimos_datos else "N/A",
                "tiempo_procesamiento": "2 segundos (simulado)",
                "timestamp": datetime.now().isoformat()
            }
            
            print(" Procesamiento STREAM completado")
            return resultado
            
        except Exception as e:
            return {"error": f"Error en stream: {str(e)}"}

# Prueba individual
if __name__ == "__main__":
    procesador = ProcesadorKappa()
    
    print(" Probando Kappa Architecture:")
    resultado_stream = procesador.procesar_stream("datos_stream.json")
    print(json.dumps(resultado_stream, indent=2))