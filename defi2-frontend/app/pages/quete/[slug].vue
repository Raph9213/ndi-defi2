<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8 flex justify-center gap-8 items-start">
    
    <!-- Left Sidebar (Completion Count) -->
    <div v-if="mission" class="hidden lg:block w-64 sticky top-24">
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 text-center">
            <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-green-100 text-green-600 mb-4">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
            </div>
            <div class="text-3xl font-black text-gray-900 mb-1">{{ mission.completions || 42 }}</div>
            <div class="text-sm font-medium text-gray-500">Valeureux guerriers ont déjà accompli cette mission !</div>
        </div>
    </div>

    <div class="max-w-3xl w-full bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100 relative">
        <!-- Loading state -->
        <div v-if="loading" class="p-12 text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
            <p class="text-gray-500">Chargement de la quête...</p>
        </div>

        <!-- Error state -->
        <div v-else-if="error" class="p-12 text-center">
            <div class="text-red-500 text-5xl mb-4">😕</div>
            <h2 class="text-2xl font-bold text-gray-900 mb-2">Oups !</h2>
            <p class="text-gray-600">{{ error }}</p>
            <NuxtLink to="/" class="mt-6 inline-block text-green-600 font-medium hover:underline">Retour à l'accueil</NuxtLink>
        </div>

        <!-- Mission Content -->
        <div v-else-if="mission" class="flex flex-col">
            <!-- Header with decorative background -->
            <div class="relative bg-green-600 h-48 flex items-center justify-center overflow-hidden">
                <div class="absolute inset-0 bg-gradient-to-br from-green-500 to-green-700 opacity-90"></div>
                <div class="absolute -bottom-10 -right-10 w-40 h-40 bg-white rounded-full opacity-10 blur-2xl"></div>
                <div class="absolute top-10 left-10 w-20 h-20 bg-yellow-300 rounded-full opacity-20 blur-xl"></div>
                
                <h1 class="relative z-10 text-4xl md:text-5xl font-extrabold text-white text-center px-4 drop-shadow-md">
                    {{ mission.name }}
                </h1>
            </div>

            <div class="p-8 md:p-12">
                <!-- Gain Badge -->
                <div class="flex justify-center -mt-16 mb-8 relative z-20">
                    <div class="bg-white rounded-2xl shadow-lg p-4 flex flex-col items-center border border-gray-100">
                        <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Empêchez l'émission de</span>
                        <div class="text-3xl font-black text-green-600 flex items-center gap-1">
                            {{ mission.co2_reduction }} <span class="text-sm font-bold text-gray-500">g CO2</span>
                        </div>
                    </div>
                </div>

                <!-- Description -->
                <div class="prose prose-lg max-w-none text-gray-600 mb-12">
                    <p>{{ mission.description }}</p>
                </div>

                <!-- Action Section -->
                <div class="bg-gray-50 rounded-2xl p-8 border border-gray-200">
                    <h3 class="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                        <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        Valider la mission
                    </h3>

                    <div v-if="!completed" class="flex items-start gap-4">
                        <div class="flex items-center h-6 mt-1">
                            <input 
                                id="complete-checkbox" 
                                type="checkbox" 
                                v-model="isChecked"
                                class="w-6 h-6 text-green-600 border-gray-300 rounded focus:ring-green-500 cursor-pointer transition-all"
                            >
                        </div>
                        <div class="flex-1">
                            <label for="complete-checkbox" class="font-medium text-gray-900 cursor-pointer select-none">
                                J'atteste sur <u>l'honneur</u>, et même sur ma dernière part de pizza, avoir réalisé cette action <strong>héroïque</strong> pour sauver la planète, un arbre, deux pingouins et peut-être même la machine à café du CROUS.
                            </label>
                            <p class="text-sm text-gray-500 mt-1">Les petits ruisseaux font les grandes rivières... et parfois même des tsunamis askip</p>
                        </div>
                    </div>

                    <div v-if="!completed" class="mt-8">
                        <button 
                            @click="completeMission" 
                            :disabled="!isChecked || isSubmitting"
                            class="w-full py-4 px-6 rounded-xl font-bold text-white text-lg shadow-md transition-all transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                            :class="isChecked ? 'bg-green-600 hover:bg-green-700 hover:shadow-lg' : 'bg-gray-400'"
                        >
                            <span v-if="isSubmitting" class="flex items-center justify-center gap-2">
                                <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                                Validation en cours...
                            </span>
                            <span v-else>Je valide ma mission ! 🫡</span>
                        </button>
                    </div>

                    <!-- Success Message -->
                    <div v-else class="bg-green-100 border border-green-200 rounded-xl p-6 text-center animate-fade-in-up">
                        <div class="text-5xl mb-4">🎉</div>
                        <h3 class="text-2xl font-bold text-green-800 mb-2">Félicitations !</h3>
                        <p class="text-green-700 mb-6">Vous avez économisé {{ mission.co2_reduction }}g de CO2. Continuez comme ça !</p>
                        <button @click="$router.go(-1)" class="text-green-700 font-semibold hover:underline">Retour aux quêtes</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute();
const router = useRouter();
const slug = route.params.slug as string;

const loading = ref(true);
const error = ref<string | null>(null);
const mission = ref<any>(null);
const isChecked = ref(false);
const isSubmitting = ref(false);
const completed = ref(false);

function slugify(s: string) {
  return encodeURIComponent(String(s).toLowerCase().replace(/\s+/g, '-'));
}

onMounted(async () => {
    try {
        const res = await fetch('https://api.raph9213.xyz/missions');
        if (!res.ok) throw new Error('Impossible de charger les missions');
        
        const missions = await res.json();
        // Find mission by slug
        mission.value = missions.find((m: any) => slugify(m.name) === slug);
        
        if (!mission.value) {
            error.value = "Cette quête n'existe pas (ou plus).";
        }
    } catch (e) {
        console.error(e);
        error.value = "Erreur de connexion au serveur.";
    } finally {
        loading.value = false;
    }
});

async function completeMission() {
    if (!isChecked.value || !mission.value) return;
    
    // Token is optional — allow fallback with username
    const raw = localStorage.getItem('ndi_token');
    const token = raw ? (raw.startsWith('Bearer ') ? raw.slice(7).trim() : raw.trim()) : null;

    isSubmitting.value = true;
    try {
        let username = sessionStorage.getItem('user_name');
        try {
            if (!username) {
                const stored = localStorage.getItem('ndi_user');
                if (stored) username = JSON.parse(stored).name;
            }
        } catch (e) {
            console.warn('Failed to parse stored user', e);
        }

        const body: any = {};
        if (username) body.user_name = username;

        const headers: any = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch(`https://api.raph9213.xyz/missions/${mission.value.id}/complete`, {
            method: 'POST',
            headers,
            body: JSON.stringify(body)
        });

        if (!res.ok) {
            const data = await res.json();
            throw new Error(data.message || 'Erreur lors de la validation');
        }

        completed.value = true;

    } catch (e: any) {
        alert(e.message);
    } finally {
        isSubmitting.value = false;
    }
}
</script>