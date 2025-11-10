/**
 * Sidebar Component Loader
 * Loads the shared sidebar component and handles initialization
 */

(async function() {
    try {
        // Fetch the sidebar component
        const response = await fetch('/components/sidebar.html');
        if (!response.ok) {
            throw new Error(`Failed to load sidebar: ${response.status}`);
        }

        const sidebarHTML = await response.text();

        // Find the sidebar container and replace it with the sidebar HTML
        const sidebarContainer = document.getElementById('sidebar-container');
        if (sidebarContainer) {
            // Create a temporary element to parse the HTML
            const temp = document.createElement('div');
            temp.innerHTML = sidebarHTML;

            // Replace the container with the actual sidebar element
            sidebarContainer.replaceWith(temp.firstElementChild);
        } else {
            console.error('Sidebar container (#sidebar-container) not found');
            return;
        }

        // Set active page based on data-page attribute
        const currentPage = document.body.getAttribute('data-page');
        if (currentPage) {
            const navItems = document.querySelectorAll('.navbar-nav .nav-item');
            navItems.forEach(item => {
                if (item.getAttribute('data-page') === currentPage) {
                    item.classList.add('active');
                }
            });
        }

        // Dispatch a custom event to signal sidebar is loaded
        // This allows page-specific scripts to initialize after sidebar is ready
        window.dispatchEvent(new CustomEvent('sidebarLoaded'));

    } catch (error) {
        console.error('Error loading sidebar:', error);
    }
})();
