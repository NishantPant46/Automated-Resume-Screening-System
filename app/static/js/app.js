document.addEventListener("DOMContentLoaded", function () {

    // Sidebar toggle

    const sidebarToggle =
        document.getElementById("sidebarToggle");

    const sidebar =
        document.querySelector(".sidebar");

    if (sidebarToggle) {

        sidebarToggle.addEventListener(
            "click",
            function () {

                sidebar.classList.toggle("active");

            }
        );

    }


    // Job search

    const search =
        document.getElementById("jobSearch");

    if (search) {

        search.addEventListener(
            "keyup",
            function () {

                const value =
                    this.value.toLowerCase();

                const rows =
                    document.querySelectorAll(
                        "#jobsTable tbody tr"
                    );

                rows.forEach(function (row) {

                    row.style.display =
                        row.innerText
                            .toLowerCase()
                            .includes(value)
                            ? ""
                            : "none";

                });

            }
        );

    }


    // Login validation

    const loginForm =
        document.getElementById("loginForm");

    if (loginForm) {

        loginForm.addEventListener(
            "submit",
            function (event) {

                const email =
                    document.querySelector(
                        "[name='email']"
                    ).value.trim();

                const password =
                    document.querySelector(
                        "[name='password']"
                    ).value.trim();

                if (!email || !password) {

                    event.preventDefault();

                    alert(
                        "Please enter email and password."
                    );

                }

            }
        );

    }

});