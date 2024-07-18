<script>
document.querySelectorAll('#navList li').forEach(function(item) {
    item.addEventListener('click', function() {
        const pageName = this.getAttribute('data-page');
        const titles = {
            'home': 'Home',
            'about': 'About Us',
            'register': 'Register',
            'login': 'Login',
            'profile': 'Your Profile',
            'profile_edit': 'Edit Your Profile',
            'menu': 'Menu',
            'booking': 'Booking',
        };
        const newTitle = titles[pageName] || titles['register'];
        document.title = newTitle;  // Update the document title
    });
});
</script>