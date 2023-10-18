<template>
    <b-container fluid class="px-0">
        <NavBar class="fixed" />
        <BooksDataTable />
        <AddBookModal />
    </b-container>
</template>
<script>
import NavBar from '~/components/NavBar.vue';
import BooksDataTable from '~/components/BooksDataTable.vue';
import appConfig from '~/config/appConfig';
import Multiselect from 'vue-multiselect';
import AddBookModal from '~/components/AddBookModal.vue';
import { ACTION_SET_BOOK_AUTHOR_OPTIONS } from '~/store-config/action.types';

export default {
    middleware: 'auth',
    async mounted() {
        const authorsFetched = await this.getAllAuthors();
        if (authorsFetched && authorsFetched.authors)
            this.$store.dispatch('books/' + ACTION_SET_BOOK_AUTHOR_OPTIONS, authorsFetched.authors);
    },
    methods: {
        async getAllAuthors() {
            return (
                await this.$axios.$get(
                    appConfig.services.library.base + appConfig.services.library.endPoints.GET_AUTHORS.path,
                    {
                        headers: { Authorization: this.$auth.strategy.token.get() },
                    }
                )
            ).data;
        },
    },
    components: { NavBar, BooksDataTable, Multiselect, AddBookModal },
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
