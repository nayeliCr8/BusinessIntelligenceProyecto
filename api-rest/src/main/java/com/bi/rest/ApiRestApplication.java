package com.bi.rest;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import java.util.*;
import java.time.LocalDateTime;

@SpringBootApplication
@RestController
@RequestMapping("/api")
public class ApiRestApplication {
    
    // Simulamos "base de datos" en memoria
    private static List<Map<String, Object>> datos = new ArrayList<>();
    
    public static void main(String[] args) {
        SpringApplication.run(ApiRestApplication.class, args);
        System.out.println("API REST ejecutándose en: http://localhost:8080");
        System.out.println("Endpoints disponibles:");
        System.out.println("   GET  /api/estadisticas");
        System.out.println("   GET  /api/datos");
        System.out.println("   POST /api/agregar");
    }
    
    // Health check
    @GetMapping
    public String hola() {
        return "API REST funcionando - " + LocalDateTime.now();
    }
    
    // Obtener estadísticas
    @GetMapping("/estadisticas")
    public Map<String, Object> getEstadisticas() {
        Map<String, Object> stats = new HashMap<>();
        stats.put("arquitectura", "REST API");
        stats.put("total_datos", datos.size());
        stats.put("timestamp", LocalDateTime.now().toString());
        
        if (!datos.isEmpty()) {
            double sumaTemp = 0;
            Set<String> dispositivos = new HashSet<>();
            
            for (Map<String, Object> dato : datos) {
                sumaTemp += (Double) dato.get("temperatura");
                dispositivos.add((String) dato.get("dispositivo"));
            }
            
            stats.put("temperatura_promedio", Math.round(sumaTemp / datos.size() * 100.0) / 100.0);
            stats.put("dispositivos_unicos", dispositivos.size());
        }
        
        return stats;
    }
    
    // Obtener todos los datos
    @GetMapping("/datos")
    public List<Map<String, Object>> getDatos() {
        return datos;
    }
    
    // Agregar nuevo dato
    @PostMapping("/agregar")
    public Map<String, Object> agregarDato(@RequestBody Map<String, Object> nuevoDato) {
        nuevoDato.put("fecha_ingreso", LocalDateTime.now().toString());
        nuevoDato.put("id", datos.size() + 1);
        datos.add(nuevoDato);
        
        Map<String, Object> respuesta = new HashMap<>();
        respuesta.put("mensaje", "Dato agregado exitosamente");
        respuesta.put("id", datos.size());
        respuesta.put("dispositivo", nuevoDato.get("dispositivo"));
        
        return respuesta;
    }
}