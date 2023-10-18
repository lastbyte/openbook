<template>
    <b-container fluid class="px-0 " style="min-height: 100vh;">
        <NavBar class="fixed" />
        <b-jumbotron class="jumbotron w-50 mx-auto my-5">
            <h1 class="display-4">Hello, Readers!</h1>
            <p class="lead">
                This is a open library,look around and find some of the best books out there. 
            </p>
            <hr class="my-4" />
            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Tempore quia magnam aspernatur nesciunt vel laborum magni eligendi sit adipisci, facere pariatur eveniet. Velit sint saepe voluptate architecto minima et repellendus.</p>
            <p class="lead">
                <a class="btn btn-primary btn-lg" href="/books" role="button">Explore Books</a>
            </p>
        </b-jumbotron>
    </b-container>
</template>

<script>
import NavBar from '~/components/NavBar.vue';

export default {
    middleware: 'auth',
    components: { NavBar },
};
</script>
