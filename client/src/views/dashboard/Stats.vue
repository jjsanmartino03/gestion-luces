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
      const data = [10.5, 9.7, 7.5, 6, 5, 8, 2];

      // Calcula el promedio de los valores en data
      const average = data.reduce((acc, val) => acc + val, 0) / data.length;

      // Convierte el promedio a formato "h h min min"
      const hours = Math.floor(average);
      const minutes = Math.round((average % 1) * 60);

      return{
        series: [{
            name: 'Horas de uso al dia',
            data: data,
          }],

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
            text: 'Promedio semanal de uso de luces',
          },
          xaxis: {
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
  }
</script>