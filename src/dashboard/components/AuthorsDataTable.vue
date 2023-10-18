<template>
    <b-container fixed class="rounded variant='dark'">
        <!-- User Interface controls -->
        <b-row class="align-item-center">
            <b-col md="9">
                <b-form-group class="my-3">
                    <b-input-group class="border rounded-pill">
                        <b-form-input
                            id="filter-input"
                            :value="dataTable.filter"
                            @input="(val) => updateDataTableValues({ filter: val })"
                            @keydown.enter.prevent="onSearch()"
                            type="text"
                            class="p-4 py-2 border-0 rounded-pill no-shadow-focus"
                            placeholder="Enter the author to search"
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
                    v-b-modal.add-author-modal
                    class="rounded border px-4 py-2 bg-primary text-white align-items-center"
                >
                    <b-icon class="mb-0" icon="plus"></b-icon> Add Author
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
            <template #cell(author_name)="row">
                <span v-html="row.value"></span>
            </template>
            <template #cell(actions)="row">
                <b-button @click="toggleRowDetails(row)" variant="primary">
                    <b-icon
                        v-if="row.detailsShowing"
                        style="font-size: medium"
                        icon="arrows-angle-contract"
                        title="collapse"
                    />
                    <b-icon
                        v-else="row.detailsShowing"
                        style="font-size: medium"
                        icon="arrows-angle-expand"
                        title="expand"
                    />
                </b-button>
                <b-button @click="showEditModal(row.item)" variant="primary">
                    <b-icon style="font-size: medium" icon="pencil-square" title="edit" />
                </b-button>
                <b-button @click="deleteAuthor(row.item.id)" variant="primary">
                    <b-icon style="font-size: medium" icon="trash-fill" title="collapse" />
                </b-button>
            </template>

            <template #row-details="row">
                <b-card class="p-3 px-5">
                    <div v-for="(value, key) in row.item" :key="key" style="vertical-align: middle">
                        <b-row v-if="key == 'name'">
                            <h4 class="text-primary">{{ value }}</h4>
                        </b-row>
                        <b-row v-if="key == 'age'" style="vertical-align: middle">
                            <span>
                                Age : <span class="text-primary">{{ value }}</span></span
                            >
                        </b-row>
                        <b-row v-if="key == 'description'" class="py-3" style="vertical-align: middle">
                            <h5>{{ value }}</h5>
                        </b-row>
                        <b-row v-if="key == 'books'" style="vertical-align: middle">
                            <p>Books Authored : {{ value.map((b) => b.name).join(', ') }}</p>
                        </b-row>
                    </div>
                </b-card>
            </template>
        </b-table>
        <b-row>
            <b-col sm="4" md="3" class="my-1">
                <b-form-group
                    label="Authors"
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
                        :options="pageOptions"
                        @input="(val) => updateDataTableValues({ perPage: val })"
                        size="sm"
                    ></b-form-select>
                </b-form-group>
            </b-col>

            <b-col sm="8" md="9" class="my-1">
                <b-pagination
                    :value="dataTable.currentPage"
                    :total-rows="dataTable.totalRows"
                    @input="
                        (val) => {
                            updateDataTableValues({ currentPage: val });
                            onCurrentPageChange(val);
                        }
                    "
                    hide-goto-end-buttons
                    pills
                    align="right"
                ></b-pagination>
            </b-col>
        </b-row>
        <UpdateAuthorModal />
    </b-container>
</template>

<script>
import appConfig from '~/config/appConfig';
import Multiselect from 'vue-multiselect';
import AddBookModal from '~/components/AddBookModal.vue';
import UpdateAuthorModal from './UpdateAuthorModal.vue';
import {
    ACTION_SET_AUTHOR_TABLE_DATA,
    ACTION_SET_AUTHOR_UPDATE,
    ACTION_SET_AUTHOR_ROW_DATA_DETAILS,
    ACTION_SET_AUTHOR_ROW_TO_UPDATE,
} from '~/store-config/action.types';

const tableConfig = {
    fields: [
        { key: 'id', label: 'ID', sortable: false, sortDirection: 'desc' },
        {
            key: 'author_name',
            label: 'name',
            sortable: false,
            formatter: (value, key, item) => {
                return `<h5>${item.name}</h5>`;
            },
        },
        { key: 'age', label: 'Age', class: 'text-center' },
        { key: 'books', label: 'No. of books', class: 'text-center' , formatter : (value, key, item) => { return value && length in value ? value.length : 0}},
        { key: 'actions', label: 'Details', class: 'text-center' },
    ],
    pageOptions: [10, 25, 50, 100, { value: 200, text: 'Show a lot' }],
    sortBy: 'name',
    sortDirection: 'asc',
};
export default {
    data() {
        return {
            ...tableConfig,
        };
    },
    computed: {
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
    async created() {
        const allAuthors = await this.getAllAuthors();
        this.$store.dispatch('authors/' + ACTION_SET_AUTHOR_TABLE_DATA, {
            items: allAuthors.authors,
            currentPage: 1,
            totalRows: allAuthors.total_count,
        });
    },
    components: { Multiselect, AddBookModal, UpdateAuthorModal },
    methods: {
        async showEditModal(data) {
            this.$store.dispatch('authors/' + ACTION_SET_AUTHOR_ROW_TO_UPDATE, { ...data });
            this.$store.dispatch('authors/' + ACTION_SET_AUTHOR_UPDATE, data);
            await this.$nextTick();
            this.$bvModal.show('update-author-modal');
        },
        async onSearch() {
            const results = (
                await this.$axios.$get(
                    appConfig.services.library.base + appConfig.services.library.endPoints.GET_AUTHORS.path,
                    {
                        params: { name: this.dataTable.filter },
                        headers: { Authorization: this.$auth.strategy.token.get() },
                    }
                )
            ).data;
            this.$store.dispatch('authors/' + ACTION_SET_AUTHOR_TABLE_DATA, {
                items: results.authors,
                currentPage: 1,
                totalRows: results.total_count,
            });
        },

        async deleteAuthor(author_id) {
            try {
                await this.$axios.$delete(
                    `${appConfig.services.library.base}${appConfig.services.library.endPoints.DELETE_AUTHOR.path}/${author_id}`,
                    {
                        headers: { Authorization: this.$auth.strategy.token.get() },
                    }
                );
                this.$toast.success('Author deleted successfully');
                const results = await this.getAllAuthors();
                this.$store.dispatch('authors/' + ACTION_SET_AUTHOR_TABLE_DATA, {
                    items: results.authors,
                    currentPage: 1,
                    totalRows: results.total_count,
                });
            } catch (error) {
                this.$toast.error('Failed to delete Author !!');
                console.log(error);
            }
        },
        async getAllAuthors(currentPage) {
            try {
                return (
                    await this.$axios.$get(
                        appConfig.services.library.base + appConfig.services.library.endPoints.GET_AUTHORS.path,
                        {
                            params: {
                                name: this.dataTable.filter,
                                page_size: this.dataTable.perPage,
                                page_no: currentPage || this.dataTable.currentPage,
                            },
                            headers: { Authorization: this.$auth.strategy.token.get() },
                        }
                    )
                ).data;
            } catch (error) {
                this.$toast.error('Failed to fetch Authors !!');
                console.log(error);
            }
        },
        toggleRowDetails(row) {
            this.$store.dispatch('authors/' + ACTION_SET_AUTHOR_ROW_DATA_DETAILS, {
                row,
            });
        },
        updateDataTableValues(values) {
            this.$store.dispatch('authors/' + ACTION_SET_AUTHOR_TABLE_DATA, values);
        },
        async onCurrentPageChange(currentPage) {
            const data = await this.getAllAuthors(currentPage);
            this.$store.dispatch('authors/' + ACTION_SET_AUTHOR_TABLE_DATA, {
                items: data.authors,
                totalRows: data.total_count,
            });
        },
    },
};
</script>
