<template>
    <b-modal hide-footer id="add-author-modal" title="Add a new Author">
        <b-form @submit="addAuthor">
            <b-form-input
                id="input-add-author-page-numbers"
                :value="addAuthorForm.id"
                type="text"
                hidden
            ></b-form-input>
            <b-form-group
                id="input-group-add-author-name"
                label="Name"
                label-for="input-add-author-name"
                description="The Name of the author to be added"
            >
                <b-form-input
                    class="form-control"
                    id="input-add-author-name"
                    :value="addAuthorForm.name"
                    @input="(val) => updateFormValues({ name: val })"
                    type="text"
                    placeholder="John Doe"
                    required
                ></b-form-input>
            </b-form-group>

            <b-form-group
                id="input-group-add-author-page-number"
                label="Age"
                label-for="input-add-author-page-numbers"
                description="How many pages does the author contain ?"
            >
                <b-form-input
                    id="input-add-author-page-numbers"
                    :value="addAuthorForm.age"
                    @input="(val) => updateFormValues({ age: val })"
                    type="number"
                    placeholder="23"
                ></b-form-input>
            </b-form-group>

            <b-form-group
                id="input-group-add-author-description"
                label="Description"
                label-for="input-add-author-description"
                description="Little bit about the book"
            >
                <b-form-textarea
                    id="input-add-author-description"
                    :value="addAuthorForm.description"
                    @input="(val) => updateFormValues({ description: val })"
                    type="textarea"
                    placeholder="This author is sick..."
                ></b-form-textarea>
            </b-form-group>

            <b-row class="justify-content-end px-2">
                <b-form-group class="m-2">
                    <b-button class="bg-info" @click="reset">
                        <b-icon icon="x-circle-fill" class="mr-2 text-white"></b-icon> Reset
                    </b-button>
                </b-form-group>
                <b-form-group class="m-2">
                    <b-button class="h5 bg-primary" type="submit">
                        <b-icon icon="save-fill" class="mr-2 text-white"></b-icon> Save</b-button
                    >
                </b-form-group>
            </b-row>
        </b-form>
    </b-modal>
</template>
<script>
import appConfig from '~/config/appConfig';
import { ACTION_SET_AUTHOR_ADD, ACTION_SET_AUTHOR_TABLE_DATA } from '~/store-config/action.types';

export default {
    computed: {
        addAuthorForm() {
            return this.$store.state.authors.addAuthor;
        },
        dataTable() {
            return {
                items: this.$store.state.authors.authorTable.items,
                totalRows: this.$store.state.authors.authorTable.totalRows,
                perPage: this.$store.state.authors.authorTable.perPage,
                currentPage: this.$store.state.authors.authorTable.currentPage,
                filter: this.$store.state.authors.authorTable.filter,
            };
        },
    },
    methods: {
        clear() {
            this.addAuthorForm = {
                id: '',
                name: '',
                age: null,
                description: '',
            };
        },
        async addAuthor(event) {
            event.preventDefault();
            try {
                const url = `${appConfig.services.library.base}${appConfig.services.library.endPoints.CREATE_AUTHOR.path}`;
                const added_author = await this.$axios.post(url, {
                    name: this.addAuthorForm.name,
                    age: this.addAuthorForm.age,
                    description: this.addAuthorForm.description,
                });
                this.$toast.success('Author added Successfully');
                this.reset();
            } catch (error) {
                console.log(error);
                this.$toast.error('Failed to add author');
            }
            try {
                this.$store.dispatch([ACTION_SET_AUTHOR_TABLE_DATA], {
                    items: added_author.author,
                    currentPage: 1,
                    totalRows: added_author.total_count,
                });
                this.reset();
            } catch (error) {
                console.log(error);
            }
        },
        async getAllAuthors() {
            try {
                return (
                    await this.$axios.get(
                        appConfig.services.library.base + appConfig.services.library.endPoints.GET_AUTHORS.path,
                        {
                            headers: { Authorization: this.$auth.strategy.token.get() },
                        }
                    )
                ).data.data;
            } catch (error) {
                this.$toast.error('Error occured while fetching author!!');
                console.log(error);
            }
        },
        close() {
            this.$bvModal.hide('add-author-modal');
        },
        updateFormValues(values) {
            this.$store.dispatch('authors/' + ACTION_SET_AUTHOR_ADD, values);
        },
        reset() {
            this.updateFormValues({
                id: '',
                name: '',
                age: null,
                description: '',
            });
        },
    },
};
</script>
