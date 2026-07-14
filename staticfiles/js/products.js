document.addEventListener("DOMContentLoaded", () => {
    alert("products js loaded");
    const searchInput = document.getElementById("searchInput");
    const filterButtons = document.querySelectorAll(".filter-btn");
    const sortSelect = document.getElementById("sortSelect");

    const productsGrid = document.getElementById("productsGrid");
    const allCards = [...document.querySelectorAll(".product-card")];

    const prevBtn = document.getElementById("prevPage");
    const nextBtn = document.getElementById("nextPage");
    const pageNumbersContainer =
        document.querySelector(".page-numbers");

    let filteredCards = [...allCards];

    let currentPage = 1;
    const productsPerPage = 100;

    /* Fade Animation */

    setTimeout(() => {
        allCards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add("show");
            }, index * 80);
        });
    }, 200);

    /* FILTER */

    function applyFilters() {

        const searchValue =
            searchInput.value.toLowerCase();

        const activeCategory =
            document.querySelector(".filter-btn.active")
            .dataset.category;

        filteredCards = allCards.filter(card => {

            const name =
                card.dataset.name;

            const category =
                card.dataset.category;

            const matchSearch =
                name.includes(searchValue);

            const matchCategory =true;
                activeCategory === "all" ||
                category.includes(activeCategory);

            return matchSearch && matchCategory;
        });

        applySorting();
    }

    /* SORTING */

    function applySorting() {

        const value = sortSelect.value;

        if(value === "low-high"){

            filteredCards.sort((a,b)=>
                parseFloat(a.dataset.price)
                -
                parseFloat(b.dataset.price)
            );
        }

        else if(value === "high-low"){

            filteredCards.sort((a,b)=>
                parseFloat(b.dataset.price)
                -
                parseFloat(a.dataset.price)
            );
        }

        else if(value === "newest"){

            filteredCards.sort((a,b)=>
                parseInt(b.dataset.date)
                -
                parseInt(a.dataset.date)
            );
        }

        currentPage = 1;
        renderProducts();
    }

    /* PAGINATION */

    function renderProducts(){

        allCards.forEach(card=>{
            card.style.display = "none";
        });

        const start =
            (currentPage - 1) * productsPerPage;

        const end =
            start + productsPerPage;

        filteredCards
            .slice(start,end)
            .forEach(card=>{
                card.style.display = "block";
            });

        createPagination();
    }

    function createPagination(){

        pageNumbersContainer.innerHTML = "";

        const totalPages =
            Math.ceil(
                filteredCards.length /
                productsPerPage
            );

        for(let i=1;i<=totalPages;i++){

            const btn =
                document.createElement("button");

            btn.classList.add("page-number");

            if(i === currentPage){
                btn.classList.add("active");
            }

            btn.textContent = i;

            btn.addEventListener("click",()=>{
                currentPage = i;
                renderProducts();
            });

            pageNumbersContainer.appendChild(btn);
        }

        prevBtn.disabled =
            currentPage === 1;

        nextBtn.disabled =
            currentPage === totalPages;
    }

    prevBtn.addEventListener("click",()=>{

        if(currentPage > 1){

            currentPage--;
            renderProducts();
        }
    });

    nextBtn.addEventListener("click",()=>{

        const totalPages =
            Math.ceil(
                filteredCards.length /
                productsPerPage
            );

        if(currentPage < totalPages){

            currentPage++;
            renderProducts();
        }
    });

    /* EVENTS */

    searchInput.addEventListener(
        "keyup",
        applyFilters
    );

    sortSelect.addEventListener(
        "change",
        applySorting
    );

    filterButtons.forEach(button=>{

        button.addEventListener("click",()=>{

            filterButtons.forEach(btn=>
                btn.classList.remove("active")
            );

            button.classList.add("active");

            applyFilters();
        });
    });

    /* Hover Enhancement */

    allCards.forEach(card => {

        card.addEventListener("mouseenter", () => {
            card.style.zIndex = "5";
        });

        card.addEventListener("mouseleave", () => {
            card.style.zIndex = "1";
        });
    });

    renderProducts();

    
});