<template>
  <apexchart
    type="pie"
    :options="chartOptions"
    :series="brandValues"
  ></apexchart>
</template>

<script>
export default {
  props: ["brandLabels", "brandValues"],
  data() {
    return {
      series: [],
      chartOptions: {
        chart: {
          width: 100,
          type: "pie",
        },
        labels: [],
        legend: {
          position: "bottom",
        },
        responsive: [
          {
            breakpoint: 480,
            options: {
              chart: {
                width: 300,
                height: 400,
              },
              legend: {
                position: "bottom",
              },
            },
          },
        ],
      },
    };
  },
  mounted() {
    this.chartOptions.labels = this.brandLabels;
  },
};
</script>
