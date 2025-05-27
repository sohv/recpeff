async function loadPapers() {
    try {
        const response = await fetch('papers.json');
        const papers = await response.json();
        
        const container = document.getElementById('papers-container');
        
        papers.forEach(paper => {
            const paperCard = document.createElement('div');
            paperCard.className = 'col-md-6 col-lg-4';
            paperCard.innerHTML = `
                <div class="card paper-card">
                    <div class="card-body">
                        <h5 class="card-title">
                            <a href="${paper.url}" class="paper-title" target="_blank">
                                ${paper.title}
                            </a>
                        </h5>
                        <h6 class="card-subtitle mb-2 text-muted">${paper.authors}</h6>
                        <p class="card-text">${paper.abstract.substring(0, 200)}...</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">${paper.published}</small>
                            <span class="badge bg-primary">${paper.category}</span>
                        </div>
                    </div>
                </div>
            `;
            container.appendChild(paperCard);
        });
    } catch (error) {
        console.error('Error loading papers:', error);
        document.getElementById('papers-container').innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger" role="alert">
                    Error loading papers. Please try again later.
                </div>
            </div>
        `;
    }
}

document.addEventListener('DOMContentLoaded', loadPapers); 