<template>
    <b-container fixed class="rounded">
        <!-- User Interface controls -->
        <b-row class="align-item-center">
            <b-col md="9">
                <b-form-group class="my-3">
                    <b-input-group class="border rounded-pill">
                        <b-form-input
                            id="filter-input"
                            :value="dataTable.filter"
                            @input="(val) => updateDataTableValues({ filter: val })"
                            type="text"
                            class="p-4 py-2 border-0 rounded-pill no-shadow-focus"
                            placeholder="Enter the book to search"
                            @keydown.enter.prevent="onSearch()"
                            debounce="100"
                        >
                        </b-form-input>
                        <b-button
                            @click="onSearch"
                            class="d-flex rounded-pill border px-5 justify-content-center align-items-center bg-primary text-white"
                        >
                            <b-icon class="h4 mb-0" icon="search"></b-icon>
                        </b-button>
                    </b-input-group>
                </b-form-group>
            </b-col>
            <b-col md="3" class="d-flex align-items-center justify-content-end">
                <b-button
                    v-b-modal.add-book-modal
                    class="rounded border px-4 py-2 bg-primary text-white align-items-center"
                >
                    <b-icon class="mb-0" icon="plus"></b-icon> Add Book
                </b-button>
            </b-col>
        </b-row>
        <!-- Main table element -->
        <b-table
        bordered
            borderless
            striped
            no-border-collapse
            hover
            outlined
            :items="dataTable.items"
            :fields="fields"
            :current-page="dataTable.currentPage"
            :per-page="dataTable.perPage"
            :filter="dataTable.filter"
            :responsive="true"
            head-variant="dark"
            show-empty
            class="rounded p-2"
            :filter-function="() => true"
        >
            <template #cell(book_name)="row">
                <span v-html="row.value"></span>
            </template>
            <template #cell(actions)="row">
                <b-button @click="toggleRowDetails(row)" variant="primary">
                    <span v-if="row.detailsShowing"> <b-icon icon="arrows-angle-contract" title="collapse" /> </span>
                    <span v-else="row.detailsShowing"> <b-icon icon="arrows-angle-expand" title="expand" /> </span>
                </b-button>
                <b-button @click="showEditModal(row.item)" variant="primary">
                    <span> <b-icon icon="pencil-square" title="edit" /> </span>
                </b-button>
                <b-button @click="deleteBook(row.item.id)" variant="primary">
                    <span> <b-icon icon="trash-fill" title="collapse" /> </span>
                </b-button>
            </template>

            <template #row-details="row">
                <b-card class="p-3 px-5">
                    <div v-for="(value, key) in row.item" :key="key">
                        <b-row v-if="key == 'name'" style="vertical-align: middle">
                            <h4 class="text-primary">{{ value }}</h4>
                        </b-row>
                        <b-row v-if="key == 'url'" style="vertical-align: middle">
                            <span
                                >Can be accessed at : <a class="text-primary">{{ value }}</a></span
                            >
                        </b-row>
                        <b-row v-if="key == 'year_published'" style="vertical-align: middle">
                            <span
                                >Published in Year : <a class="text-primary">{{ value }}</a></span
                            >
                        </b-row>
                        <b-row v-if="key == 'authors'" style="vertical-align: middle">
                            <span
                                >Writeen by :
                                <span class="text-primary">{{ value.map((a) => a.name).join(' ,') }}</span></span
                            >
                        </b-row>
                        <b-row v-if="key == 'description'" style="vertical-align: middle" class="py-3">
                            <p>{{ value }}</p>
                        </b-row>
                    </div>
                </b-card>
            </template>
        </b-table>
        <b-row>
            <b-col sm="4" md="3" class="my-1">
                <b-form-group
                    label="Books"
                    label-for="per-page-select"
                    label-cols-sm="6"
                    label-cols-md="4"
                    label-cols-lg="3"
                    label-align-sm="right"
                    label-size="sm"
                    class="mb-0"
                >
                    <b-form-select
                        id="per-page-select"
                        :value="dataTable.perPage"
                        @input="(val) => updateDataTableValues({ perPage: val })"
                        :options="pageOptions"
                        size="sm"
                    ></b-form-select>
                </b-form-group>
            </b-col>

            <b-col sm="8" md="9" class="my-1">
                <b-pagination
                    :value="dataTable.currentPage"
                    :total-rows="dataTable.totalRows"
                    hide-goto-end-buttons
                    pills
                    @input="
                        (val) => {
                            updateDataTableValues({ currentPage: val });
                            onCurrentPageChange(val);
                        }
                    "
                    align="right"
                ></b-pagination>
            </b-col>
        </b-row>
        <UpdateBookModal />
    </b-container>
</template>

<script>
import appConfig from '~/config/appConfig';
import Multiselect from 'vue-multiselect';
import AddBookModal from '~/components/AddBookModal.vue';
import UpdateBookModal from './UpdateBookModal.vue';
import {
    ACTION_SET_BOOK_TABLE_DATA,
    ACTION_SET_BOOK_ROW_DATA_DETAILS,
    ACTION_SET_BOOK_ROW_TO_UPDATE,
    ACTION_SET_BOOK_UPDATE,
} from '~/store-config/action.types';

const tableConfig = {
    fields: [
        { key: 'id', label: 'ID', sortable: false, sortDirection: 'desc' },
        {
            key: 'book_name',
            label: 'Title',
            sortable: false,
            formatter: (value, key, item) => {
                return `<h6>${item.name}</h6>`;
            },
        },
        { key: 'page_numbers', label: 'No. of pages', sortable: false, class: 'text-center' },
        {
            key: 'authors',
            label: 'Authors',
            sortable: false,
            class: 'text-center',
            formatter: (value, key, item) => {
                const numWriters = value ? value.map((a) => a.name).length : 0;
                return numWriters + (numWriters > 1 ? ' Writers' : ' Writer');
            },
        },
        { key: 'actions', label: 'Actions', class: 'text-center' },
    ],
    pageOptions: [10, 25, 50, 100, { value: 200, text: 'Show a lot' }],
    sortBy: 'name',
    sortDirection: 'asc',
};
export default {
    data() {
        return {
            ...tableConfig,
            editBookForm: {
                name: '',
                page_numbers: null,
                year_published: null,
                url: '',
                description: '',
                authors: [],
            },
        };
    },
    computed: {
        dataTable() {
            return {
                items: this.$store.state.books.bookTable.items,
                totalRows: this.$store.state.books.bookTable.totalRows,
                authors: this.$store.state.books.bookTable.authorOptions,
                perPage: this.$store.state.books.bookTable.perPage,
                currentPage: this.$store.state.books.bookTable.currentPage,
                filter: this.$store.state.books.bookTable.filter,
            };
        },
    },
    async created() {
        const updatedBooks = await this.getAllBooks();
        this.$store.dispatch('books/' + ACTION_SET_BOOK_TABLE_DATA, {
            items: updatedBooks.books,
            currentPage: 1,
            totalRows: updatedBooks.total_count,
        });
    },

    methods: {
        async showEditModal(data) {
            this.$store.dispatch('books/' + ACTION_SET_BOOK_ROW_TO_UPDATE, { ...data });
            this.$store.dispatch('books/' + ACTION_SET_BOOK_UPDATE, data);
            await this.$nextTick();
            this.$bvModal.show('update-book-modal');
        },
        async onSearch() {
            const results = (
                await this.$axios.$get(
                    appConfig.services.library.base + appConfig.services.library.endPoints.GET_BOOKS.path,
                    {
                        params: {
                            name: this.dataTable.filter,
                            page_size: this.dataTable.perPage,
                            page_no: this.dataTable.currentPage,
                        },
                        headers: { Authorization: this.$auth.strategy.token.get() },
                    }
                )
            ).data;
            this.$store.dispatch('books/' + ACTION_SET_BOOK_TABLE_DATA, {
                items: results.books,
                totalRows: results.total_count,
            });
        },
        async deleteBook(book_id) {
            try {
                await this.$axios.$delete(
                    `${appConfig.services.library.base}${appConfig.services.library.endPoints.DELETE_BOOK.path}/${book_id}`,
                    {
                        headers: { Authorization: this.$auth.strategy.token.get() },
                    }
                );
                this.$toast.success('Book deleted successfully !!');
                const results = (
                    await this.$axios.$get(
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
                ).data;
                this.$store.dispatch('books/' + ACTION_SET_BOOK_TABLE_DATA, {
                    items: results.books,
                    totalRows: results.total_count,
                });
            } catch (error) {
                this.$toast.error('Failed to delete Book !!');
                console.log(error);
            }
        },
        async getAllBooks(currentPage) {
            try {
                return (
                    await this.$axios.$get(
                        appConfig.services.library.base + appConfig.services.library.endPoints.GET_BOOKS.path,
                        {
                            headers: { Authorization: this.$auth.strategy.token.get() },
                            params: {
                                name: this.dataTable.filter,
                                page_size: this.dataTable.perPage,
                                page_no: currentPage || this.dataTable.currentPage,
                            },
                        }
                    )
                ).data;
            } catch (error) {
                this.$toast.error('Failed to fetch Books !!');
                console.log(error);
            }
        },
        toggleRowDetails(row) {
            this.$store.dispatch('books/' + ACTION_SET_BOOK_ROW_DATA_DETAILS, {
                row,
            });
        },
        updateDataTableValues(values) {
            this.$store.dispatch('books/' + ACTION_SET_BOOK_TABLE_DATA, values);
        },
        async onCurrentPageChange(currentPage) {
        const data = await this.getAllBooks(currentPage);
        this.$store.dispatch('books/' + ACTION_SET_BOOK_TABLE_DATA, { items: data.books, totalRows: data.total_count });
    },
    },
    components: { Multiselect, AddBookModal, UpdateBookModal },
};
</script>
