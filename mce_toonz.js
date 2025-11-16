const webtoonContainer = document.getElementById('webtoon-container');
const carouselDisplay = document.getElementById('carousel-display');
const carouselLeft = document.getElementById('carousel-left');
const carouselRight = document.getElementById('carousel-right');
const carouselHeader = document.getElementById('carousel-header');
const pdfDownloadBtn = document.getElementById('pdf-download-btn');

// Configuration and state
let config = null;
let currentDirectoryIndex = 0;
let currentIndex = 0;

// Load configuration
async function loadConfig() {
    try {
        const response = await fetch('config.json');
        config = await response.json();
        updateCarousel();
    } catch (error) {
        console.error('Error loading config:', error);
        carouselDisplay.textContent = 'Error loading configuration';
    }
}

// Update carousel display and buttons
function updateCarousel() {
    if (!config || !config.directories.length) return;
    
    const currentDirectory = config.directories[currentDirectoryIndex];
    carouselDisplay.textContent = currentDirectory.description;
    
    // Update button states
    carouselLeft.disabled = currentDirectoryIndex === 0;
    carouselRight.disabled = currentDirectoryIndex === config.directories.length - 1;
    
    // Update PDF download button
    if (currentDirectory.pdfFile) {
        pdfDownloadBtn.href = currentDirectory.pdfFile;
        pdfDownloadBtn.download = `${currentDirectory.name}.pdf`;
        pdfDownloadBtn.classList.remove('disabled');
    } else {
        pdfDownloadBtn.href = '#';
        pdfDownloadBtn.removeAttribute('download');
        pdfDownloadBtn.classList.add('disabled');
    }
    
    // Load images for current directory
    loadImages(currentDirectory);
}

// Load images for selected directory
function loadImages(directory) {
    // Clear existing images
    webtoonContainer.innerHTML = '';
    
    // Create image elements
    directory.files.forEach(fileName => {
        const imgElement = document.createElement('img');
        imgElement.src = `mce_toonz/${directory.name}/${fileName}`;
        imgElement.alt = fileName;
        webtoonContainer.appendChild(imgElement);
    });
    
    // Reset scroll position immediately
    currentIndex = 0;
    webtoonContainer.scrollTop = 0;
    webtoonContainer.scrollTo(0, 0);
}

// Carousel navigation
carouselLeft.addEventListener('click', () => {
    if (currentDirectoryIndex > 0) {
        currentDirectoryIndex--;
        updateCarousel();
    }
});

carouselRight.addEventListener('click', () => {
    if (config && currentDirectoryIndex < config.directories.length - 1) {
        currentDirectoryIndex++;
        updateCarousel();
    }
});

// Přidání funkcionality pro scrollování
function handleScroll(event) {
    event.preventDefault();
    const images = webtoonContainer.querySelectorAll('img');
    
    if (images.length === 0) return;
    
    const delta = event.deltaY;
    const threshold = 50; // Minimum scroll distance to trigger change

    if (Math.abs(delta) > threshold) {
        if (delta > 0 && currentIndex < images.length - 1) {
            currentIndex++;
            scrollToCurrentIndex();
        } else if (delta < 0 && currentIndex > 0) {
            currentIndex--;
            scrollToCurrentIndex();
        }
    }
}

function scrollToCurrentIndex() {
    const images = webtoonContainer.querySelectorAll('img');
    if (images.length === 0 || !images[currentIndex]) return;
    
    // Scroll to specific image with offset for header
    const headerHeight = document.getElementById('carousel-header').offsetHeight;
    const imagePosition = images[currentIndex].offsetTop - headerHeight;
    
    webtoonContainer.scrollTo({
        top: imagePosition,
        behavior: 'smooth'
    });
}

// Přidání posluchače událostí pro scrollování
window.addEventListener('wheel', handleScroll);

// Initialize on page load
loadConfig();