// JS for Certificate Section

const modal = document.getElementById("certModal");
const modalImg = document.getElementById("certImage");
const captionText = document.getElementById("caption");
const span = document.getElementsByClassName("close-btn")[0];
const certCards = document.querySelectorAll('.cert-card');

function openCertModal(imageSrc, title) {
    modal.style.display = "block";
    modalImg.src = imageSrc;
    captionText.innerHTML = title;
}

certCards.forEach(card => {
    const button = card.querySelector('.view-cert-btn');
    const imageSrc = card.getAttribute('data-cert-image');
    const title = card.querySelector('h3').textContent;
    button.addEventListener('click', () => {
        openCertModal(imageSrc, title);
    });
});
function closeCertModal() {
    modal.style.display = "none";
}
span.onclick = closeCertModal;
window.onclick = function(event) {
    if (event.target == modal) {
        closeCertModal();
    }
}


// JS for Project Section

const projectsExpandedPanel = document.getElementById('project-details-expanded');
let currentActiveProjectId = null;

function generateDetailsHTML(project) {
    const featuresHTML = project.features.map(f => `<li>${f}</li>`).join('');

    const imagesHTML = project.images.map(img =>
        `<img src="${img.src}" alt="${project.name} Screenshot" class="gallery-image" data-caption="${img.caption}">`
    ).join('');

    return `
        <div class="details-content">
            <div class="details-left">
                <h4>${project.name}</h4>
                <p class="project-description">${project.description}</p>

                <div class="features-block">
                    <h5>Key Features:</h5>
                    <ul class="features-list">${featuresHTML}</ul>
                </div>

                <p class="tech-stack">Tech Stack:${project.techStack}</p>

            </div>

            <div class="details-right">
                <div class="image-gallery">
                    <div class="gallery-track">${imagesHTML}</div>
                    <button class="gallery-nav prev-btn">&#10094;</button>
                    <button class="gallery-nav next-btn">&#10095;</button>
                </div>
                <p class="gallery-caption"></p>

                <div class="project-links">
                    <a href="${project.links.github}" target="_blank" class="link-btn github-btn">GitHub Repo</a>
                    ${project.links.live ? `<a href="${project.links.live}" target="_blank" class="link-btn live-btn">Live Application</a>` : ''}
                    ${project.links.video2 ? `<a href="${project.links.video2}" target="_blank" class="link-btn live-btn">Video Demo2</a>` : ''}
                    ${project.links.video ? `<a href="${project.links.video}" target="_blank" class="link-btn demo-btn">Video Demo</a>` : ''}
                </div>
            </div>
        </div>
    `;
}

// 2. Project Detail Toggle Functionality
document.querySelectorAll('.project-card').forEach(card => {
    card.style.borderColor = card.getAttribute('data-theme-color');
    card.querySelector('h3').style.color = card.getAttribute('data-theme-color');

    card.addEventListener('click', () => {
        const projectId = parseInt(card.getAttribute('data-project-id'));
        const themeColor = card.getAttribute('data-theme-color');
        const project = projectData.find(p => p.id === projectId);

        // --- Toggle Logic ---
        if (currentActiveProjectId === projectId) {
            projectsExpandedPanel.style.height = '0';
            projectsExpandedPanel.classList.remove('open');
            card.classList.remove('active');
            currentActiveProjectId = null;
        } else {
            // Switch to a new panel
            // 1. Deactivate old card
            document.querySelectorAll('.project-card').forEach(c => c.classList.remove('active'));

            // 2. Activate new card
            card.classList.add('active');
            currentActiveProjectId = projectId;

            // 3. Update Content and Theme
            projectsExpandedPanel.innerHTML = generateDetailsHTML(project);
            projectsExpandedPanel.style.borderColor = themeColor;

            // 4. Force Height Recalculation (for smooth transition)
            projectsExpandedPanel.classList.add('open');
            setTimeout(() => {
                const contentHeight = projectsExpandedPanel.querySelector('.details-content').offsetHeight;
                projectsExpandedPanel.style.height = `${contentHeight + 60}px`;
                setupGallery(projectsExpandedPanel);
            }, 10);
        }
    });
});


// 3. Image Gallery Carousel with Sliding Animation
function setupGallery(projectDetailsElement) {
    const gallery = projectDetailsElement.querySelector('.image-gallery');
    const track = gallery.querySelector('.gallery-track');
    const images = gallery.querySelectorAll('.gallery-image');
    const captionElement = projectDetailsElement.querySelector('.gallery-caption');
    const prevBtn = gallery.querySelector('.prev-btn');
    const nextBtn = gallery.querySelector('.next-btn');
    let currentIndex = 0;

    // Function to update the view
    function updateGallery() {
        const imageWidth = images[0].offsetWidth;
        const offset = -currentIndex * imageWidth;
        track.style.transform = `translateX(${offset}px)`;

        // Update caption (Request 6)
        captionElement.textContent = images[currentIndex].getAttribute('data-caption');
    }

    prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        updateGallery();
    });

    nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % images.length;
        updateGallery();
    });
    if (images.length > 0) {
        window.addEventListener('resize', updateGallery);

        // Initial setup
        updateGallery();
    }
}
