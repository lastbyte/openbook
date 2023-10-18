<template>
    <div>
        <b-navbar toggleable="lg" variant="primary">
            <b-navbar-brand href="/">OpenBook</b-navbar-brand>

            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav>
                    <b-nav-item href="/books">Books</b-nav-item>
                    <b-nav-item href="/authors">Authors</b-nav-item>
                </b-navbar-nav>
                <b-navbar-nav class="ml-auto">
                    <b-nav-item-dropdown right v-if="username !== null" variant="primary">
                        <template #button-content>
                            <b-icon icon="gear-wide-connected" aria-hidden="true"></b-icon>
                            {{ username }}
                        </template>
                        <b-dropdown-item href="#"  @click="logout" class="body d-flex justify-content-center align-items-center"
                            ><b-icon icon="power" class="mr-2" aria-hidden="true"></b-icon>Logout</b-dropdown-item
                        >
                    </b-nav-item-dropdown>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>
</template>
<script>
export default {
    data () {
        return {
            username : this.$auth.user.username
        }
    },
    methods : {
        async logout() {
            await this.$auth.logout();
            // Redirect to the login page or another route
            this.$router.push('/login')
        },
    }
};
</script>
