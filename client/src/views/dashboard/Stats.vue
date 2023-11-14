<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="chart-container" id="chart" >
    <apexchart type="bar" height="380" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>

<style scoped>
</style>

<style>
  .chart-container {
    background-color: #F1FAF6;
    border: 1px solid #ccc; /* Agrega un borde al contenedor */
    border-radius: 10px;    /* Aplica esquinas redondeadas */
    padding: 15px;          /* Agrega un espacio interno para dar margen al contenido */
    width: 90%;           /* Ancho deseado para el contenedor (ajusta según tus necesidades) */
    margin: 0 auto;         /* Centra el contenedor horizontalmente */
  }
  body {
    background-color: #E8ECEA;
  }
</style>

<script>
  import VueApexCharts from "vue3-apexcharts"
  export default{
    components: {
      apexchart: VueApexCharts,
    },
    data() {
      const data = [8.5, 9.7, 7.5, 6, 5, 8, 2];

      // Calcula el promedio de los valores en data
      const average = data.reduce((acc, val) => acc + val, 0) / data.length;

      // Convierte el promedio a formato "h h min min"
      const hours = Math.floor(average);
      const minutes = Math.round((average % 1) * 60);

      return{
        series: [
          {
            name: 'Horas de uso al día',
            data: [10.5, 9.7, 7.5, 6, 5, 8, 2], // Actualiza los datos del gráfico con los promedios recibidos
          },
        ],

        chartOptions: {
          chart: {
            type: 'bar',
            height: 350
          },
          plotOptions: {
            bar: {
              horizontal: false,
              columnWidth: '55%',
              endingShape: 'rounded'
            },
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
          },
          title: {
            text: `${hours} h ${minutes} min`,
            style: {
            fontSize: '25px', // Tamaño de fuente deseado
            color: '#333', // Color de texto deseado
            fontWeight: 'bold', // Estilo de fuente deseado
          },
          },
          subtitle: {
            text:`Promedio semanal de uso de luces `,
            style: {
            fontSize: '13px',
            },
          },
          xaxis: {
            title: {
            text: `${this.calcularFechasDeLaSemana().inicio} - ${this.calcularFechasDeLaSemana().fin}`,
            style: {
              fontSize: '13px',
            },
          },
            categories: ['D', 'L', 'M', 'M', 'J', 'V', 'S'],
          },
          yaxis: {
            opposite: true,
            labels: {
              formatter: (val) => {
                return val + ' hs'
              }
            }
          },
          fill: {
            opacity: 1
          },
          tooltip: {
            y: {
              formatter: function (val) {
                return  val + " hs"
              }
            }
          }
        },
      } 
    },
    methods: {
      calcularFechasDeLaSemana() {
        const fechaActual = new Date();
        const diaDeLaSemana = fechaActual.getDay();

        const fechaDelDomingo = new Date(fechaActual);
        fechaDelDomingo.setDate(fechaActual.getDate() - diaDeLaSemana);

        const fechaDelSabado = new Date(fechaDelDomingo);
        fechaDelSabado.setDate(fechaDelDomingo.getDate() + 6); // Sábado es 6 días después de domingo

        const diaDomingo = fechaDelDomingo.getDate();
        const mesDomingo = fechaDelDomingo.getMonth() + 1;
        const añoDomingo = fechaDelDomingo.getFullYear();

        const diaSabado = fechaDelSabado.getDate();
        const mesSabado = fechaDelSabado.getMonth() + 1;
        const añoSabado = fechaDelSabado.getFullYear();

        const fechaInicio = `${diaDomingo < 10 ? '0' : ''}${diaDomingo}/${mesDomingo < 10 ? '0' : ''}${mesDomingo}/${añoDomingo}`;
        const fechaFin = `${diaSabado < 10 ? '0' : ''}${diaSabado}/${mesSabado < 10 ? '0' : ''}${mesSabado}/${añoSabado}`;

        return { inicio: fechaInicio, fin: fechaFin };
      },
      enviarFechaAlBackend() {
        const fechaDelDomingo = this.calcularFechasDeLaSemana().inicio; // Obtén la fecha del domingo
        // Realiza una solicitud GET al backend con la fecha
        axios.get(`http://127.0.0.1:8000/api/estadistica_semanal/?fecha_domingo=${fechaDelDomingo}`)
          .then(response => {
            // Maneja la respuesta del backend que contiene la lista de promedios
            const promedios = response.data; // Suponiendo que la respuesta es una lista de números
            this.series = [
              {
                name: 'Horas de uso al día',
                data: promedios, // Actualiza los datos del gráfico con los promedios recibidos
              },
            ];
          })
          .catch(error => {
            // Maneja errores
            console.error(error);
          });
      },
    },
    mounted() {
      // Llama a la función para enviar la fecha al backend automáticamente al cargar la página
      //this.enviarFechaAlBackend();
    },
  }
</script>