const { ApolloServer, gql } = require('apollo-server');

// Datos en memoria
let sensorData = [
  {
    id: "1",
    dispositivo: "sensor_25",
    temperatura: 25.5,
    humedad: 60.0,
    presion: 1013.2,
    bateria: 85,
    timestamp: new Date().toISOString()
  }
];

// Schema GraphQL
const typeDefs = gql`
  type SensorData {
    id: ID!
    dispositivo: String!
    temperatura: Float!
    humedad: Float!
    presion: Float!
    bateria: Int!
    timestamp: String!
  }

  type Stats {
    totalDatos: Int!
    dispositivosUnicos: Int!
    temperaturaPromedio: Float!
    temperaturaMaxima: Float!
    temperaturaMinima: Float!
  }

  type Query {
    hola: String
    todosLosDatos: [SensorData!]!
    estadisticas: Stats!
    datosPorDispositivo(dispositivo: String!): [SensorData!]!
  }

  type Mutation {
    agregarDato(
      dispositivo: String!
      temperatura: Float!
      humedad: Float!
      presion: Float!
      bateria: Int!
    ): SensorData!
  }
`;

// Resolvers
const resolvers = {
  Query: {
    hola: () => "¡Hola desde GraphQL! ",
    
    todosLosDatos: () => sensorData,
    
    estadisticas: () => {
      if (sensorData.length === 0) {
        return {
          totalDatos: 0,
          dispositivosUnicos: 0,
          temperaturaPromedio: 0,
          temperaturaMaxima: 0,
          temperaturaMinima: 0
        };
      }
      
      const temps = sensorData.map(d => d.temperatura);
      const dispositivosUnicos = new Set(sensorData.map(d => d.dispositivo));
      
      return {
        totalDatos: sensorData.length,
        dispositivosUnicos: dispositivosUnicos.size,
        temperaturaPromedio: parseFloat((temps.reduce((a, b) => a + b, 0) / temps.length).toFixed(2)),
        temperaturaMaxima: parseFloat(Math.max(...temps).toFixed(2)),
        temperaturaMinima: parseFloat(Math.min(...temps).toFixed(2))
      };
    },
    
    datosPorDispositivo: (_, { dispositivo }) => {
      return sensorData.filter(d => d.dispositivo === dispositivo);
    }
  },
  
  Mutation: {
    agregarDato: (_, { dispositivo, temperatura, humedad, presion, bateria }) => {
      const newData = {
        id: String(sensorData.length + 1),
        dispositivo,
        temperatura,
        humedad,
        presion,
        bateria,
        timestamp: new Date().toISOString()
      };
      
      sensorData.push(newData);
      return newData;
    }
  }
};

// Crear servidor
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: true,
  playground: true
});

// Iniciar
server.listen({ port: 4000 }).then(({ url }) => {
  console.log(" API GraphQL ejecutándose en: " + url);
  console.log(" Playground disponible en: " + url);
  console.log(" Query de ejemplo:");
  console.log(`{
    estadisticas {
      totalDatos
      temperaturaPromedio
    }
    todosLosDatos {
      dispositivo
      temperatura
    }
  }`);
});