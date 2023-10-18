export default {
    // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
    ssr: false,

    // Target: https://go.nuxtjs.dev/config-target
    target: 'static',

    // Global page headers: https://go.nuxtjs.dev/config-head
    head: {
        title: 'DC Full Stack Code Challenge',
        htmlAttrs: {
            lang: 'en',
        },
        meta: [
            { charset: 'utf-8' },
            {
                name: 'viewport',
                content: 'width=device-width, initial-scale=1',
            },
            { hid: 'description', name: 'description', content: '' },
            { name: 'format-detection', content: 'telephone=no' },
        ],
        link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
    },

    // Global CSS: https://go.nuxtjs.dev/config-css
    css: ['@/assets/css/main.css'],

    // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
    plugins: [],

    // Auto import components: https://go.nuxtjs.dev/config-components
    components: true,

    // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
    buildModules: [
        // https://go.nuxtjs.dev/typescript
        '@nuxt/typescript-build',
        '@nuxtjs/toast',
    ],

    // Modules: https://go.nuxtjs.dev/config-modules
    modules: [
        // https://go.nuxtjs.dev/bootstrap
        ['bootstrap-vue/nuxt', { icons: true, css: true }],
        // https://go.nuxtjs.dev/axios
        '@nuxtjs/axios',
        '@nuxtjs/auth-next',
        'cookie-universal-nuxt',
    ],
    toast: {
        position: 'top-right',
        duration : '2000'
    },
    auth: {
        strategies: {
            local: {
                token: {
                    property: 'token',
                    global: true,
                    maxAge: 24 * 3600,
                    type: 'Bearer',
                },
                user: {
                    property: 'user',
                    autoFetch: true,
                },
                endpoints: {
                    login: {
                        url: 'http://localhost:8000/api/auth/login',
                        method: 'post',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    },
                    logout: { url: 'http://localhost:8000/api/auth/logout', method: 'post' },
                    user: { url: 'http://localhost:8000/api/auth/current-user', method: 'post' },
                },
                redirect: {
                    login: '/login', // Redirect to the login page
                    home: '/', // Redirect to the dashboard after login
                    logout: '/login', // Redirect to the home page after logout
                },
            },
        },
    },

    publicRuntimeConfig: {
        axios: {
            baseURL: process.env.BASEURL || 'http://127.0.0.1:8000',
        },
    },

    // Axios module configuration: https://go.nuxtjs.dev/config-axios
    axios: {
        // Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
        baseURL: process.env.NODE_ENV == 'development' ? 'http://127.0.0.1:8000' : process.env.BASEURL,
    },

    // Build Configuration: https://go.nuxtjs.dev/config-build
    build: {},
};
