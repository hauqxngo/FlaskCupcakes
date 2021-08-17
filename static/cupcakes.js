const BASE_URL = "http://localhost:5000/api";

function generateCupcakeHTML(cupcake) {
    return `
        <div data-cupcake-id=${cupcake.id}>
            <li>
                ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
                <button class="delete-button btn btn-danger btn-sm">x</button>
            </li>

            <img class="cupcake-img" src="${cupcake.image}"  
        </div>
    `;
}


// Put cupcakes on page
async function showCupcakes() {
    const res = await axios.get(`${BASE_URL}/cupcakes`);

    for (let cupcakeData of res.data.cupcake) {
        let newCupcake = $(generateCupcakeHTML(cupcakeData));
        $("#cupcakes-list").append(newCupcake);
    }
}


// Handle form for adding a new cupcake
$("#new-cupcake-form").on("submit", async function(e) {
    e.preventDefault();

    let flavor = $("#flavor").val();
    let rating = $("#rating").val();
    let size = $("#size").val();
    let image = $("#image").val();

    const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });

    let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
});


// Handle clicking to delete cupcake

$("#cupcakes-list").on("click", ".delete-button", async function(e) {
    e.preventDefault();
    let $cupcake = $(e.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});


$(showCupcakes);