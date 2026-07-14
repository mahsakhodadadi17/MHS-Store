document.addEventListener("DOMContentLoaded", function () {


    const productsGrid = document.getElementById("productsGrid");

    const products = Array.from(
        document.querySelectorAll(".product-card")
    );


    const sortSelect = document.getElementById("sortSelect");


    const searchInput = document.getElementById("searchInput");


    const filterButtons = document.querySelectorAll(".filter-btn");



    let currentCategory = "all";





    function renderProducts(){


        let result = [...products];



        // دسته بندی

        if(currentCategory !== "all"){


            result = result.filter(product => {


                return product.dataset.category.includes(
                    currentCategory
                );


            });


        }





        // جستجو

        let searchValue = searchInput.value.toLowerCase();



        result = result.filter(product=>{


            return product.dataset.name.includes(searchValue);


        });







        // مرتب سازی


        let sortValue = sortSelect.value;



        if(sortValue === "low-high"){


            result.sort((a,b)=>{


                return Number(a.dataset.price) - Number(b.dataset.price);


            });


        }





        else if(sortValue === "high-low"){


            result.sort((a,b)=>{


                return Number(b.dataset.price) - Number(a.dataset.price);


            });


        }





        else if(sortValue === "newest"){


            result.sort((a,b)=>{


                return Number(b.dataset.date) - Number(a.dataset.date);


            });


        }







        // نمایش


        productsGrid.innerHTML = "";



        result.forEach(product=>{


            productsGrid.appendChild(product);


        });




    }







    // دکمه های دسته بندی


    filterButtons.forEach(button=>{


        button.addEventListener("click",function(){



            filterButtons.forEach(btn=>{


                btn.classList.remove("active");


            });




            this.classList.add("active");



            currentCategory = this.dataset.category;



            renderProducts();



        });


    });







    // سرچ


    searchInput.addEventListener(
        "input",
        renderProducts
    );





    // مرتب سازی


    sortSelect.addEventListener(
        "change",
        renderProducts
    );





});