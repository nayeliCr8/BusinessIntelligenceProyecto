import requests
import time
import statistics
import json
from datetime import datetime

class ProbadorRendimiento:
    def __init__(self):
        self.resultados = []
    
    def probar_endpoint(self, nombre, url, metodo='GET', datos=None, headers=None):
        """Prueba un endpoint y mide tiempo de respuesta"""
        print(f"\n Probando: {nombre}")
        print(f"   URL: {url}")
        
        tiempos = []
        exitosos = 0
        
        for i in range(5):  # 5 pruebas
            try:
                inicio = time.time()
                
                if metodo == 'GET':
                    response = requests.get(url, timeout=10, headers=headers)
                else:
                    response = requests.post(url, json=datos, timeout=10, headers=headers)
                
                fin = time.time()
                
                if response.status_code == 200:
                    tiempo_ms = (fin - inicio) * 1000
                    tiempos.append(tiempo_ms)
                    exitosos += 1
                    print(f" -> Prueba {i+1}: {tiempo_ms:.2f} ms")
                else:
                    print(f" -> Prueba {i+1}: Error {response.status_code}")
                    
            except Exception as e:
                print(f" -> Prueba {i+1}: Error - {str(e)}")
            
            time.sleep(1)  # Espera entre pruebas
        
        # Guardar resultados
        if tiempos:
            resultado = {
                'nombre': nombre,
                'url': url,
                'pruebas_totales': 5,
                'pruebas_exitosas': exitosos,
                'tiempo_promedio_ms': statistics.mean(tiempos),
                'tiempo_minimo_ms': min(tiempos),
                'tiempo_maximo_ms': max(tiempos),
                'fecha_prueba': datetime.now().isoformat()
            }
            
            self.resultados.append(resultado)
            
            print(f"\n    RESULTADOS {nombre}:")
            print(f"      Tiempo promedio: {resultado['tiempo_promedio_ms']:.2f} ms")
            print(f"      Rango: {resultado['tiempo_minimo_ms']:.2f} - {resultado['tiempo_maximo_ms']:.2f} ms")
            print(f"      Éxitos: {resultado['pruebas_exitosas']}/5")
        
        return tiempos
    
    def comparar_arquitecturas(self):
        """Compara Lambda vs Kappa"""
        print(" COMPARANDO ARQUITECTURAS DE INGESTA:")
        
        # Probar Lambda
        lambda_batch = self.probar_endpoint(
            "LAMBDA - Batch Processing", 
            "http://localhost:8080/api/estadisticas"
        )
        
        # Probar Kappa (simulado)
        kappa_stream = self.probar_endpoint(
            "KAPPA - Stream Processing", 
            "http://localhost:4000/graphql",
            'POST',
            {"query": "{ estadisticas { totalDatos temperaturaPromedio } }"},
            {"Content-Type": "application/json"}
        )
        
        return lambda_batch, kappa_stream
    
    def comparar_apis(self):
        """Compara REST vs GraphQL"""
        print(" COMPARANDO APIS:")
        
        # REST API
        rest_stats = self.probar_endpoint(
            "REST API - Estadísticas", 
            "http://localhost:8080/api/estadisticas"
        )
        
        # GraphQL API
        graphql_stats = self.probar_endpoint(
            "GraphQL API - Estadísticas",
            "http://localhost:4000/graphql",
            'POST',
            {"query": "{ estadisticas { totalDatos temperaturaPromedio } }"},
            {"Content-Type": "application/json"}
        )
        
        return rest_stats, graphql_stats
    
    def ejecutar_pruebas_completas(self):
        """Ejecuta todas las pruebas"""
        print(" INICIANDO PRUEBAS DE RENDIMIENTO COMPLETAS")
        print("=" * 60)
        
        print("Ojo:  Asegurarme de tener ejecutando:")
        print("   - API REST: http://localhost:8080")
        print("   - API GraphQL: http://localhost:4000")
        
        input("\nPresiona Enter para iniciar las pruebas...")
        
        # Ejecutar pruebas
        self.comparar_apis()
        self.comparar_arquitecturas()
        
        # Guardar resultados
        with open('resultados/benchmark.json', 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)
        
        print("\n ¡TODAS LAS PRUEBAS COMPLETADAS!")
        print(" Resultados guardados en: resultados/benchmark.json")
        
        # Mostrar resumen
        print("\n" + "=" * 60)
        print(" RESUMEN FINAL:")
        for resultado in self.resultados:
            print(f"   {resultado['nombre']}: {resultado['tiempo_promedio_ms']:.2f} ms")

# Ejecutar pruebas
if __name__ == "__main__":
    probador = ProbadorRendimiento()
    probador.ejecutar_pruebas_completas()