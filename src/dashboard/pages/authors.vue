<template>
    <b-container fluid class="px-0">
        <NavBar class="fixed" />
        <AuthorsDataTable />
        <AddAuthorModal />
    </b-container>
</template>
<script>
import NavBar from '~/components/NavBar.vue';
import Multiselect from 'vue-multiselect';
import AddAuthorModal from '~/components/AddAuthorModal.vue';
import UpdateAuthorModal from '~/components/UpdateAuthorModal.vue';
import AuthorsDataTable from '~/components/AuthorsDataTable.vue';

export default {
    middleware: 'auth',
    updated() {},
    methods: {},
    components: { NavBar, Multiselect, AddAuthorModal, UpdateAuthorModal, AuthorsDataTable },
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
