"use strict";
const ctx = document.getElementById("chart").getContext("2d");

const get_data = async (url) => {
  const response = await fetch(url, {
    method: "GET",
  });
  return response.json();
};

const create_dataset = (data) => {
  let dataset = [];
  data.usernames.forEach((element) => {
    dataset.push({
      label: element,
      data: data.points[element],
      spanGaps: true,
    });
  });
  return dataset;
};

const url = location.href.replace(/ranking/, "ranking-chart");
const ranking_data = get_data(url).then((data) => {
  const chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: data.datetime,
      datasets: create_dataset(data),
    },
    options: {
      elements: {
        line: {
          tension: 0,
        },
      },
      scales: {
        yAxes: [
          {
            scaleLabel: {
              display: true,
              labelString: "Points",
            },
            ticks: {
              min: 0,
            },
          },
        ],
        xAxes: [
          {
            type: "time",
          },
        ],
      },
      plugins: {
        colorschemes: {
          scheme: "tableau.Tableau10",
        },
      },
    },
  });
});
