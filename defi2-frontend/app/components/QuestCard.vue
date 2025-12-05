<template>
    <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-6 flex flex-col h-full transition-transform hover:-translate-y-1 hover:shadow-xl duration-300">
        <h5 class="mb-3 text-xl font-bold text-gray-900">{{ props.title }}</h5>
        <p class="text-gray-600 mb-6 flex-grow">{{ props.description }}</p>
        
        <div class="mt-auto">
            <NuxtLink :to="'/quete/' + props.slug" class="inline-flex items-center justify-center w-full text-white bg-green-600 hover:bg-green-700 font-medium rounded-xl text-sm px-5 py-3 transition-colors focus:outline-none focus:ring-4 focus:ring-green-200">
                Voir la quête
                <svg class="w-4 h-4 ms-2 rtl:rotate-180" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
                </svg>
            </NuxtLink>
        </div>
    </div>
</template>

<script setup lang="ts">
interface Props {
    title: string;
    description: string;
    gain: number;
    temps: number;
    slug: string;
}

const props = defineProps<Props>();
</script>