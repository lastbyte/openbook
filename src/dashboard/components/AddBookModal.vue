<template>
    <b-modal hide-footer id="add-book-modal" title="Add a new Book">
        <b-form @submit="addBook">
            <b-form-input
                id="input-add-book-name"
                :value="addBookForm.id"
                type="text"
                placeholder="The Wierd Theory"
                hidden
                :state="null"
            ></b-form-input>
            <b-form-group
                id="input-group-add-book-name"
                label="Name"
                label-for="input-add-book-name"
                description="The Name of the book to be added"
            >
                <b-form-input
                    id="input-add-book-name"
                    :value="addBookForm.name"
                    @input="(val) => updateFormValues({ name: val })"
                    type="text"
                    placeholder="The Wierd Theory"
                    required
                ></b-form-input>
            </b-form-group>

            <b-form-group
                id="input-group-add-book-page-number"
                label="Number of pages"
                label-for="input-add-book-page-numbers"
                description="How many pages does the book contain ?"
            >
                <b-form-input
                    id="input-add-book-page-numbers"
                    :value="addBookForm.page_numbers"
                    @input="(val) => updateFormValues({ page_numbers: parseInt(val) })"
                    type="number"
                    placeholder="234"
                    required
                ></b-form-input>
            </b-form-group>
            <b-form-group
                id="input-group-add-book-authors"
                label="Authors"
                label-for="input-add-book-authors"
                description="Credits to the writers"
            >
                <multiselect
                    :value="addBookForm.authors"
                    @input="(val) => updateFormValues({ authors: val })"
                    :options="authors"
                    :multiple="true"
                    :close-on-select="false"
                    :clear-on-select="false"
                    :preserve-search="true"
                    placeholder="Select Authors"
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
                id="input-group-add-book-year-published"
                label="Publication year"
                label-for="input-add-book-page-numbers"
                description="When was it published ?"
                required
            >
                <b-form-input
                    id="input-add-book-page-numbers"
                    :value="addBookForm.year_published"
                    @input="(val) => updateFormValues({ year_published: parseInt(val) })"
                    type="number"
                    placeholder="1995"
                ></b-form-input>
            </b-form-group>

            <b-form-group
                id="input-group-add-book-ul"
                label="Online url"
                label-for="input-add-book-url"
                description="Where can I access it ?"
            >
                <b-form-input
                    id="input-add-book-url"
                    :value="addBookForm.url"
                    @input="(val) => updateFormValues({ url: val })"
                    type="url"
                    placeholder="https://bit.ly/fewr4f"
                ></b-form-input>
            </b-form-group>
            <b-form-group
                id="input-group-add-book-description"
                label="Description"
                label-for="input-add-book-description"
                description="Little bit about the book"
            >
                <b-form-textarea
                    id="input-add-book-description"
                    :value="addBookForm.description"
                    @input="(val) => updateFormValues({ description: val })"
                    type="textarea"
                    placeholder="This book is about blah blah blah ..."
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
import { toInteger } from 'lodash';
import Multiselect from 'vue-multiselect';
import appConfig from '~/config/appConfig';
import { ACTION_SET_BOOK_ADD } from '~/store-config/action.types';
export default {
    components: { Multiselect },

    computed: {
        addBookForm() {
            return this.$store.state.books.addBook;
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
        async addBook(event) {
            event.preventDefault();
            try {
                if (!this.addBookForm.authors) {
                    this.$toast.alert('Select an author');
                    return;
                }
                const url = `${appConfig.services.library.base}${appConfig.services.library.endPoints.CREATE_BOOK.path}`;
                const added_book = await this.$axios.post(url, {
                    name: this.addBookForm.name,
                    page_numbers: this.addBookForm.page_numbers,
                    year_published: this.addBookForm.year_published,
                    url: this.addBookForm.url,
                    description: this.addBookForm.description,
                    authors: this.addBookForm.authors ? this.addBookForm.authors.map((a) => a.id) : [],
                });
                this.$toast.success('Book added Successfully');
                this.reset();
            } catch (error) {
                this.$toast.error('Failed to add Book');
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
        close() {
            this.$bvModal.hide('add-book-modal');
        },
        reset() {
            this.updateFormValues({
                name: '',
                page_numbers: null,
                year_published: null,
                url: '',
                description: '',
                authors: [],
            });
        },
        updateFormValues(values) {
            this.$store.dispatch('books/' + ACTION_SET_BOOK_ADD, values);
        },
    },
};
</script>
