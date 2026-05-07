
(function () {
    const messages = {
        "/ats-checker": {
            title: "Analisando currículo",
            subtitle: "Estamos lendo seu PDF e preparando a análise ATS.",
            steps: [
                "Recebendo currículo",
                "Extraindo texto do PDF",
                "Analisando critérios ATS",
                "Gerando recomendações"
            ]
        },
        "/humanizer": {
            title: "Humanizando texto",
            subtitle: "Estamos deixando seu texto mais natural e profissional.",
            steps: [
                "Recebendo texto",
                "Identificando tom e estrutura",
                "Reescrevendo com IA",
                "Finalizando versão humanizada"
            ]
        },
        "/ai-detector": {
            title: "Analisando texto",
            subtitle: "Estamos verificando padrões de escrita artificial.",
            steps: [
                "Recebendo texto",
                "Mapeando padrões",
                "Avaliando sinais de IA",
                "Gerando sugestões"
            ]
        },
        "/linkedin-generator": {
            title: "Gerando perfil LinkedIn",
            subtitle: "Estamos criando uma apresentação profissional.",
            steps: [
                "Recebendo informações",
                "Organizando experiência",
                "Criando texto profissional",
                "Finalizando perfil"
            ]
        }
    };

    function setText(id, value) {
        const element = document.getElementById(id);
        if (element) element.textContent = value;
    }

    function configureSteps(stepLabels) {
        const steps = document.querySelectorAll(".ai-step");
        steps.forEach((step, index) => {
            const label = stepLabels[index];
            if (label) {
                step.childNodes[step.childNodes.length - 1].textContent = " " + label;
            }
            step.classList.remove("active", "done");
            if (index === 0) step.classList.add("active");
        });
    }

    function activateStep(index) {
        const steps = document.querySelectorAll(".ai-step");
        steps.forEach((step, stepIndex) => {
            step.classList.remove("active", "done");
            if (stepIndex < index) step.classList.add("done");
            if (stepIndex === index) step.classList.add("active");
        });
    }

    function showLoading(form) {
        const overlay = document.getElementById("aiLoadingOverlay");
        const progressBar = document.getElementById("aiProgressBar");
        const progressText = document.getElementById("aiProgressText");
        const stepText = document.getElementById("aiStepText");

        if (!overlay || !progressBar || !progressText || !stepText) return;

        const config = messages[form.getAttribute("action")] || {
            title: "Processando com IA",
            subtitle: "Estamos preparando sua resposta.",
            steps: ["Recebendo dados", "Preparando conteúdo", "Consultando IA", "Gerando resultado"]
        };

        setText("loadingTitle", config.title);
        setText("loadingSubtitle", config.subtitle);
        configureSteps(config.steps);

        overlay.classList.add("show");
        overlay.setAttribute("aria-hidden", "false");

        let progress = 4;
        let currentStep = 0;
        progressBar.style.width = progress + "%";
        progressText.textContent = progress + "%";
        stepText.textContent = config.steps[currentStep];

        const intervals = [
            { limit: 24, step: 0, speed: 280 },
            { limit: 48, step: 1, speed: 420 },
            { limit: 74, step: 2, speed: 620 },
            { limit: 92, step: 3, speed: 820 }
        ];

        let intervalIndex = 0;

        const timer = setInterval(() => {
            const current = intervals[intervalIndex] || intervals[intervals.length - 1];

            if (progress < current.limit) {
                progress += Math.max(1, Math.round(Math.random() * 4));
            } else if (intervalIndex < intervals.length - 1) {
                intervalIndex++;
                currentStep = intervals[intervalIndex].step;
                activateStep(currentStep);
                stepText.textContent = config.steps[currentStep];
            } else {
                progress = Math.min(progress + 1, 96);
            }

            progress = Math.min(progress, 96);
            progressBar.style.width = progress + "%";
            progressText.textContent = progress + "%";
        }, 520);

        window.__toolflowLoadingTimer = timer;
    }

    document.querySelectorAll("form").forEach((form) => {
        form.addEventListener("submit", () => {
            const button = form.querySelector("button[type='submit'], button");
            if (button) {
                button.disabled = true;
                button.classList.add("is-loading");
                button.dataset.originalText = button.innerText;
                button.innerText = "Processando";
            }

            showLoading(form);
        });
    });
})();
