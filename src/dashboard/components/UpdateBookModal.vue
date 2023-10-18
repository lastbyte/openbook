<template>
    <b-modal id="update-book-modal" title="Update Book" hide-footer>
        <b-form @submit="updateBook">
            <b-form-group
                id="input-group-author-book-name"
                label="Name"
                label-for="input-author-book-name"
                description="The Name of the book to be added"
            >
                <b-form-input
                    id="input-author-book-name"
                    :value="editBookForm.name"
                    @input="(val) => updateFormValues({ name: val })"
                    type="text"
                    placeholder="The Wierd Theory"
                    required
                ></b-form-input>
            </b-form-group>

            <b-form-group
                id="input-group-author-book-page-number"
                label="Number of pages"
                label-for="input-author-book-page-numbers"
                description="How many pages does the book contain ?"
            >
                <b-form-input
                    id="input-author-book-page-numbers"
                    :value="editBookForm.page_numbers"
                    @input="(val) => updateFormValues({ page_numbers: val })"
                    type="number"
                    placeholder="234"
                    required
                ></b-form-input>
            </b-form-group>
            <b-form-group
                id="input-group-author-book-authors"
                label="Authors"
                label-for="input-author-book-authors"
                description="Credits to the writers"
            >
                <multiselect
                    :value="editBookForm.authors"
                    @input="(val) => updateFormValues({ authors: val })"
                    :options="this.$store.state.books.authorOptions"
                    :multiple="true"
                    :close-on-select="false"
                    :clear-on-select="false"
                    :preserve-search="true"
                    placeholder="Pick some"
                    label="name"
                    track-by="id"
                >
                    <template slot="selection" slot-scope="{ values, search, isOpen }"
                        ><span class="multiselect__single" v-if="values ? values.length : false" v-show="!isOpen"
                            >{{ values ? values.length : 0 }} options selected</span
                        ></template
                    >
                </multiselect>
            </b-form-group>
            <b-form-group
                id="input-group-author-book-year-published"
                label="Publication year"
                label-for="input-author-book-page-numbers"
                description="When was it published ?"
            >
                <b-form-input
                    id="input-author-book-page-numbers"
                    :value="editBookForm.year_published"
                    @input="(val) => updateFormValues({ year_published: val })"
                    type="number"
                    placeholder="1995"
                ></b-form-input>
            </b-form-group>

            <b-form-group
                id="input-group-author-book-ul"
                label="Online url"
                label-for="input-author-book-url"
                description="Where can I access it ?"
            >
                <b-form-input
                    id="input-author-book-url"
                    :value="editBookForm.url"
                    @input="(val) => updateFormValues({ url: val })"
                    type="url"
                    placeholder="https://bit.ly/fewr4f"
                ></b-form-input>
            </b-form-group>
            <b-form-group
                id="input-group-author-book-description"
                label="Description"
                label-for="input-author-book-description"
                description="Little bit about the book"
            >
                <b-form-textarea
                    id="input-author-book-description"
                    :value="editBookForm.description"
                    @input="(val) => updateFormValues({ description: val })"
                    type="textarea"
                    placeholder="This book is about blah blah blah ..."
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
import Multiselect from 'vue-multiselect';
import appConfig from '~/config/appConfig';
import { ACTION_SET_BOOK_TABLE_DATA, ACTION_SET_BOOK_UPDATE } from '~/store-config/action.types';

export default {
    components: { Multiselect },
    computed: {
        editBookForm() {
            return this.$store.state.books.updateBook;
        },
        authors() {
            return this.$store.state.books.authorOptions;
        },
        dataTable() {
            return {
                items: this.$store.state.books.bookTable.items,
                totalRows: this.$store.state.books.bookTable.totalRows,
                perPage: this.$store.state.books.bookTable.perPage,
                currentPage: this.$store.state.books.bookTable.currentPage,
                filter: this.$store.state.books.bookTable.filter,
            };
        },
    },
    methods: {
        async updateBook(event) {
            event.preventDefault();
            try {
                const url = `${appConfig.services.library.base}${
                    appConfig.services.library.endPoints.UPDATE_BOOK.path
                }/${this.editBookForm ? this.editBookForm.id : ''}`;
                console.log(url);
                await this.$axios.put(url, {
                    name: this.editBookForm ? this.editBookForm.name : '',
                    page_numbers: this.editBookForm ? this.editBookForm.page_numbers : null,
                    description: this.editBookForm ? this.editBookForm.description : '',
                    year_published: this.editBookForm ? this.editBookForm.year_published : null,
                    url: this.editBookForm ? this.editBookForm.url : '',
                    authors: this.editBookForm ? this.editBookForm.authors.map((cb) => cb.id) : [],
                });
                this.$toast.success('Book updated successfully!!');
            } catch (error) {
                this.$toast.error('Book update failed !!');
                console.log(error);
            }
            try {
                const updatedBooks = await this.getAllBooks();
                this.$store.dispatch('books/' + ACTION_SET_BOOK_TABLE_DATA, {
                    items: updatedBooks.books,
                    currentPage: 1,
                    totalRows: updatedBooks.total_count,
                });
            } catch (error) {
                console.log(error);
            }
        },
        async getAllBooks() {
            try {
                return (
                    await this.$axios.get(
                        appConfig.services.library.base + appConfig.services.library.endPoints.GET_BOOKS.path,
                        {
                            headers: { Authorization: this.$auth.strategy.token.get() },
                            params: {
                                name: this.dataTable.filter,
                                page_size: this.dataTable.perPage,
                                page_no: this.dataTable.currentPage,
                            },
                        }
                    )
                ).data.data;
            } catch (error) {
                this.$toast.error('Error occured while fetching books!!');
                console.log(error);
            }
        },
        reset() {
            this.updateFormValues(this.$store.state.books.rowToUpdate)
        },
        updateFormValues(values) {
            this.$store.dispatch('books/' + ACTION_SET_BOOK_UPDATE, values);
        },
    },
};
</script>
