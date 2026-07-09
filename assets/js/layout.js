async function carregarLayout() {

    try {

        const header = await fetch("/cyberdimension-site/header.html");
        const footer = await fetch("/cyberdimension-site/footer.html");

        document.getElementById("header").innerHTML =
            await header.text();

        document.getElementById("footer").innerHTML =
            await footer.text();

    } catch (erro) {

        console.error("Erro ao carregar layout:", erro);

    }

}

carregarLayout();