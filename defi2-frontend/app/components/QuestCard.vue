<template>
    <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-6 flex flex-col h-full transition-transform hover:-translate-y-1 hover:shadow-xl duration-300">
        <h5 class="mb-3 text-xl font-bold text-gray-900">{{ title }}</h5>
        <p class="text-gray-600 mb-6 flex-grow">{{ description }}</p>
        <p class="text-gray-600 mb-6 flex-grow font-bold text-green-600"><span class="text-sm font-medium text-gray-500">Vous empêcherez l'émission de </span>{{ gain }} g CO2</p>

        <div class="flex gap-2 mt-auto">
            <NuxtLink :to="'/quete/' + slug" class="inline-flex items-center justify-center flex-1 text-white bg-green-600 hover:bg-green-700 font-medium rounded-xl text-sm px-5 py-3 transition-colors focus:outline-none focus:ring-4 focus:ring-green-200">
                Voir la quête
            </NuxtLink>
            <button @click="complete" class="inline-flex items-center justify-center flex-none text-green-700 border border-green-600 hover:bg-green-50 font-medium rounded-xl text-sm px-4 py-2 transition-colors">Compléter</button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
const props = defineProps<{
    id?: number;
    title: string;
    description: string;
    gain?: number;
    temps?: number;
    slug: string;
}>();
const emit = defineEmits(['completed']);

const title = props.title;
const description = props.description;
const slug = props.slug;

async function complete() {
    const token = localStorage.getItem('ndi_token');
    if (!token) {
        alert('Veuillez vous connecter pour compléter cette mission.');
        return;
    }
    try {
        console.log('Completing mission:', props.id);
        console.log('Token:', token);
        const res = await fetch(`http://4.tcp.eu.ngrok.io:12316/missions/${props.id}/complete`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
        });
        const data = await res.json();
        if (!res.ok) {
            alert(data.message || 'Erreur lors de la complétion');
            return;
        }
        emit('completed', data);
    } catch (e) {
        console.error(e);
        alert('Impossible de contacter l\'API');
    }
}
</script>