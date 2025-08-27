import json
import time
import random
from datetime import datetime
import os

class GeneradorDatos:
    def __init__(self):
        self.contador = 0
         
        os.makedirs("lambda-architecture", exist_ok=True)
        os.makedirs("kappa-architecture", exist_ok=True)
    
    def generar_dato_sensor(self):
        """Genera datos de sensores IoT"""
        self.contador += 1
        return {
            "id": self.contador,
            "timestamp": datetime.now().isoformat(),
            "dispositivo": f"sensor_{random.randint(1, 100)}",
            "temperatura": round(random.uniform(20.0, 35.0), 2),
            "humedad": round(random.uniform(30.0, 80.0), 2),
            "presion": round(random.uniform(1000.0, 1020.0), 2),
            "bateria": random.randint(10, 100)
        }
    
    def guardar_dato(self, dato, archivo):
        """Guarda datos en archivo JSON"""
        try:
            with open(archivo, 'a', encoding='utf-8') as f:
                f.write(json.dumps(dato, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Error guardando: {e}")
    
    def simular_flujo_datos(self, datos_por_segundo=1):
        """Simula flujo continuo de datos"""
        print("INICIANDO GENERADOR DE DATOS")
        print("=" * 50)
        print("Datos guardados en:")
        print("   - lambda-architecture/datos_batch.json (Procesamiento LENTO)")
        print("   - lambda-architecture/datos_realtime.json (Procesamiento RAPIDO)")
        print("   - kappa-architecture/datos_stream.json (Procesamiento STREAM)")
        print("Presiona CTRL + C para detener")
        print("=" * 50)
        
        try:
            while True:
                dato = self.generar_dato_sensor()
                
                # Para Lambda Architecture (2 procesamientos)
                self.guardar_dato(dato, "lambda-architecture/datos_batch.json")
                self.guardar_dato(dato, "lambda-architecture/datos_realtime.json")
                
                # Para Kappa Architecture (1 procesamiento)
                self.guardar_dato(dato, "kappa-architecture/datos_stream.json")
                
                print(f"Dato {self.contador}: {dato['dispositivo']} - {dato['temperatura']}C")
                time.sleep(1 / datos_por_segundo)
                
        except KeyboardInterrupt:
            print(f"\nGeneracion completada! Total: {self.contador} datos")

# Ejecutar
if __name__ == "__main__":
    generador = GeneradorDatos()
    generador.simular_flujo_datos(datos_por_segundo=2)