/**
 * Empêche l'accès à une page utilisateur si le nom de l'utilisateur ne correspond pas à celui stocké dans le sessionStorage
 */
export default defineNuxtRouteMiddleware((to, from) => {
    if (process.client) {
        const storedName = sessionStorage.getItem('user_name');
        const targetName = to.params.id;
        if (!storedName || storedName !== targetName) {
            if (storedName) {
                window.location.href = '/';
            }
            window.location.href = '/';
        }
    }
});
