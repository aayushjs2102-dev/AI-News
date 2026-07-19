/*
====================================================
AI News Recommendation System
Main JavaScript File

Author: Aayush
====================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    initializeAssistant();

    initializeAnalytics();

});


/* ==================================================
   AI Assistant
================================================== */

function initializeAssistant() {

    const form = document.getElementById("assistant-form");

    if (!form) {
        return;
    }

    const button = document.getElementById("ask-button");
    const textarea = document.getElementById("question");

    if (textarea) {

        textarea.focus();

        textarea.addEventListener("keydown", (event) => {

            if (event.key === "Enter" && event.ctrlKey) {

                event.preventDefault();

                form.requestSubmit();

            }

        });

    }

    form.addEventListener("submit", () => {

        if (button) {

            button.disabled = true;

            button.innerHTML = "⏳ Retrieving articles...";

        }

    });

    const conversation = document.querySelector(".conversation");

    if (conversation) {

        conversation.scrollIntoView({

            behavior: "smooth",

            block: "start"

        });

    }

}


/* ==================================================
   Analytics Dashboard
================================================== */

function initializeAnalytics() {

    if (typeof Chart === "undefined") {
        return;
    }

    createClusterChart();

    createSourceChart();

}


/* ==================================================
   Cluster Chart
================================================== */

function createClusterChart() {

    const canvas = document.getElementById("clusterChart");

    if (!canvas || !window.clusterData) {
        return;
    }

    new Chart(canvas, {

        type: "bar",
        indexAxis: "y",

        data: {

            labels: window.clusterData.labels,

            datasets: [

                {

                    label: "Articles",

                    data: window.clusterData.values,

                    borderWidth: 1

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: true,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                y: {

                    beginAtZero: true,

                    ticks: {

                        precision: 0

                    }

                }

            }

        }

    });

}


/* ==================================================
   Source Chart
================================================== */

function createSourceChart() {

    const canvas = document.getElementById("sourceChart");

    if (!canvas || !window.sourceData) {
        return;
    }

    new Chart(canvas, {

        type: "bar",
        indexAxis: "y",

        data: {

            labels: window.sourceData.labels,

            datasets: [

                {

                    label: "Articles",

                    data: window.sourceData.values,

                    borderWidth: 1

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                y: {

                    beginAtZero: true,

                    ticks: {

                        precision: 0

                    }

                }

            }

        }

    });

}