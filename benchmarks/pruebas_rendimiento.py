import requests
import time
import statistics
import json
from datetime import datetime
import psutil  #CPU y memoria

class ProbadorRendimiento:
    def __init__(self):
        self.resultados = []
    
    def probar_endpoint(self, nombre, url, metodo='GET', datos=None, headers=None):
        """Prueba un endpoint y mide tiempo de respuesta, latencia, CPU, memoria y throughput"""
        print(f"\n Probando: {nombre}")
        print(f"   URL: {url}")
        
        tiempos = []
        latencias = []
        exitosos = 0
        
        #metricas iniciales de sistema
        cpu_inicial = psutil.cpu_percent(interval=0.5)
        memoria_inicial = psutil.virtual_memory().percent
        
        inicio_total = time.time()
        
        for i in range(50):  #50 pruebas
            try:
                inicio = time.time()
                
                if metodo == 'GET':
                    response = requests.get(url, timeout=10, headers=headers)
                else:
                    response = requests.post(url, json=datos, timeout=10, headers=headers)
                
                fin = time.time()
                
                if response.status_code == 200:
                    tiempo_ms = (fin - inicio) * 1000
                    latencia_ms = response.elapsed.total_seconds() * 1000
                    
                    tiempos.append(tiempo_ms)
                    latencias.append(latencia_ms)
                    exitosos += 1
                    
                    print(f" -> Prueba {i+1}: {tiempo_ms:.2f} ms (latencia {latencia_ms:.2f} ms)")
                else:
                    print(f" -> Prueba {i+1}: Error {response.status_code}")
                    
            except Exception as e:
                print(f" -> Prueba {i+1}: Error - {str(e)}")
            
            time.sleep(1)  # Espera entre pruebas
        
        fin_total = time.time()
        total_duracion = fin_total - inicio_total
        
        #metricas finales de sistema
        cpu_final = psutil.cpu_percent(interval=0.5)
        memoria_final = psutil.virtual_memory().percent
        
        if tiempos:
            throughput = exitosos / total_duracion
            
            resultado = {
                'nombre': nombre,
                'url': url,
                'pruebas_totales': 50,
                'pruebas_exitosas': exitosos,
                'tiempo_promedio_ms': statistics.mean(tiempos),
                'tiempo_minimo_ms': min(tiempos),
                'tiempo_maximo_ms': max(tiempos),
                'latencia_promedio_ms': statistics.mean(latencias) if latencias else None,
                'cpu_inicial_%': cpu_inicial,
                'cpu_final_%': cpu_final,
                'memoria_inicial_%': memoria_inicial,
                'memoria_final_%': memoria_final,
                'throughput_req_s': throughput,
                'fecha_prueba': datetime.now().isoformat()
            }
            
            self.resultados.append(resultado)
            
            print(f"\n    RESULTADOS {nombre}:")
            print(f"      Tiempo promedio: {resultado['tiempo_promedio_ms']:.2f} ms")
            print(f"      Latencia promedio: {resultado['latencia_promedio_ms']:.2f} ms")
            print(f"      CPU: {cpu_inicial:.2f}% -> {cpu_final:.2f}%")
            print(f"      Memoria: {memoria_inicial:.2f}% -> {memoria_final:.2f}%")
            print(f"      Throughput: {throughput:.2f} req/s")
        
        return tiempos
    
    def ejecutar_pruebas_completas(self):
        print(" INICIANDO PRUEBAS DE RENDIMIENTO COMPLETAS")
        print("=" * 60)
        
        print("Ojo: Asegurarse de tener ejecutando:")
        print("   - API REST: http://localhost:8080")
        print("   - API GraphQL: http://localhost:4000")
        
        input("\nPresiona Enter para iniciar las pruebas...")
        
        #Resgt API
        self.probar_endpoint(
            "REST API - Estadísticas", 
            "http://localhost:8080/api/estadisticas"
        )
        
        #GraphQL API
        self.probar_endpoint(
            "GraphQL API - Estadísticas",
            "http://localhost:4000/graphql",
            'POST',
            {"query": "{ estadisticas { totalDatos temperaturaPromedio } }"},
            {"Content-Type": "application/json"}
        )
        
        #Guardar resultados
        with open('resultados/benchmark.json', 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)
        
        print("\n ¡TODAS LAS PRUEBAS COMPLETADAS!")
        print(" Resultados guardados en: resultados/benchmark.json")

# Ejecutar
if __name__ == "__main__":
    probador = ProbadorRendimiento()
    probador.ejecutar_pruebas_completas()
