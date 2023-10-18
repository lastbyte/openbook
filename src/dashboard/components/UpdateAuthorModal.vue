\<template>
    <b-modal hide-footer id="update-author-modal" title="Update Author">
        <b-form @submit="updateAuthor">
            <b-form-input
                id="input-edit-author-page-numbers"
                :value="editAuthorForm.id"
                type="text"
                hidden
            ></b-form-input>
            <b-form-group
                id="input-group-edit-author-name"
                label="Name"
                label-for="input-edit-author-name"
                description="The Name of the author to be edited"
            >
                <b-form-input
                    id="input-edit-author-name"
                    :value="editAuthorForm.name"
                    type="text"
                    @input="(val) => updateFormValues({name : val})"
                    placeholder="John Doe"
                    required
                ></b-form-input>
            </b-form-group>

            <b-form-group
                id="input-group-edit-author-page-number"
                label="Age"
                label-for="input-edit-author-page-numbers"
                description="How many pages does the author contain ?"
            >
                <b-form-input
                    id="input-edit-author-page-numbers"
                    :value="editAuthorForm.age"
                    type="number"
                    @input="(val) => updateFormValues({age : val})"
                    placeholder="23"
                ></b-form-input>
            </b-form-group>

            <b-form-group
                id="input-group-edit-author-description"
                label="Description"
                label-for="input-edit-author-description"
                description="Little bit about the author"
            >
                <b-form-textarea
                    id="input-edit-author-description"
                    :value="editAuthorForm.description"
                    @input="(val) => updateFormValues({description : val})"
                    type="textarea"
                    placeholder="This author is sick..."
                ></b-form-textarea>
            </b-form-group>

            <b-row class="justify-content-end px-2">
                <b-form-group class="m-2">
                    <b-button class="bg-info" @click="reset">
                        <b-icon icon="x-circle-fill" class="mr-2 text-white"></b-icon>Reset</b-button
                    >
                </b-form-group>
                <b-form-group class="m-2">
                    <b-button class="h5 bg-primary" type="submit">
                        <b-icon icon="save-fill" class="mr-2 text-white"></b-icon>Save</b-button
                    >
                </b-form-group>
            </b-row>
        </b-form>
    </b-modal>
</template>
<script>
import appConfig from '~/config/appConfig';
import { ACTION_SET_AUTHOR_TABLE_DATA, ACTION_SET_AUTHOR_UPDATE} from '~/store-config/action.types';
export default {
    computed: {
        authors() {
            return this.$store.state.authors.authorOptions;
        },
        editAuthorForm() {
            return this.$store.state.authors.updateAuthor;
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
        async updateAuthor(event) {
            event.preventDefault();
            try {
                const url = `${appConfig.services.library.base}${
                    appConfig.services.library.endPoints.UPDATE_AUTHOR.path
                }/${this.editAuthorForm.id ? this.editAuthorForm.id : ''}`;
                console.log(url);
                await this.$axios(url, {
                    method: 'put',
                    data: {
                        id: this.editAuthorForm.id,
                        name: this.editAuthorForm.name,
                        description: this.editAuthorForm.description,
                        age: this.editAuthorForm.age,
                    },
                });
                const updatedAuthors = await this.getAllAuthors();
                this.$store.dispatch('authors/'+ACTION_SET_AUTHOR_TABLE_DATA, {
                    items: updatedAuthors.authors,
                    currentPage: 1,
                    totalRows: updatedAuthors.total_count,
                });
                this.$toast.success('Author updated successfully!!');
            } catch (error) {
                this.$toast.error('Author update failed !!');
                console.log(error);
            }
        },
        async getAllAuthors() {
            try {
                return (
                    await this.$axios.get(
                        appConfig.services.library.base + appConfig.services.library.endPoints.GET_AUTHORS.path,
                        {   
                            params: { name: this.dataTable.filter, page_size: this.dataTable.perPage, page_no: this.dataTable.currentPage },
                            headers: { Authorization: this.$auth.strategy.token.get() },
                        }
                    )
                ).data.data;
            } catch (error) {
                this.$toast.error('Error occured while fetching author!!');
                console.log(error);
            }
        },
        reset() {
            this.updateFormValues(this.$store.state.authors.rowToUpdate)
        },
        updateFormValues(values) {
            this.$store.dispatch('authors/'+ACTION_SET_AUTHOR_UPDATE, values);
        }
    },
};
</script>
