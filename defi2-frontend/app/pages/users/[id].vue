<template>
  <div class="min-h-screen bg-gray-50 pb-10 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <!-- User Profile Section -->
        <div class="bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100 flex flex-col lg:col-span-1">
          <div class="h-48 overflow-hidden">
            <img class="w-full h-full object-cover" src="/no_ppl.webp" alt="User Profile">
          </div>
          <div class="p-8 flex flex-col flex-grow">
            <div class="uppercase tracking-wide text-sm text-green-600 font-semibold">Votre identité</div>
            <h1 class="mt-2 text-3xl font-extrabold tracking-tight text-gray-900">
              {{ $route.params.id }}
            </h1>
            <div class="mt-6 flex items-center">
              <div class="flex-shrink-0 bg-green-100 rounded-full p-3">
                <svg class="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-5">
                <p class="text-lg font-medium text-gray-900">Impact Écologique</p>
                <p class="mt-1 text-2xl font-bold text-green-600">{{ formatSavedCo(savedCO) }} <span class="text-sm font-medium text-gray-500">de CO2 évité</span></p>
              </div>
            </div>
          </div>
        </div>

        <!-- Tribe Section -->
        <Tribe v-if="customVillage" :customVillage="customVillage" />

        <!-- No Tribe State -->
        <NoTribe v-else @create="handleCreateTribe" @join="handleJoinTribe" />

      </div>

      <!-- Quests Section -->
      <div class="mt-12">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path></svg>
          Quêtes disponibles
        </h2>
        
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <QuestCard
              v-for="m in missions"
              :key="m.id"
              :id="m.id"
              :title="m.name"
              :description="m.description"
              :gain="m.co2_reduction"
              :temps="m.temps || 0"
              :slug="slugify(m.name)"
              @completed="onMissionCompleted"
            />
          </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
const route = useRoute();
const savedCO = ref<number>(0);

const missions = ref<Array<any>>([]);

function slugify(s: string) {
  return encodeURIComponent(String(s).toLowerCase().replace(/\s+/g, '-'));
}

const customVillage = ref<any>(null);

const handleCreateTribe = async (name: string) => {
  try {
    const res = await fetch('http://4.tcp.eu.ngrok.io:12316/api/tribe/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ owner_name: route.params.id, name })
    });
    if (!res.ok) {
      const err = await res.json();
      alert(err.message || 'Erreur lors de la création de la tribu');
      return;
    }
    const data = await res.json();
    customVillage.value = data;
  } catch (e) {
    console.error(e);
    alert('Impossible de contacter l\'API');
  }
};

const formatSavedCo = (co: number): string => {
  if (co < 1000) {
    return `${co} g`;
  }
  const kg = co / 1000;
  if (kg < 1000) {
    return `${kg.toLocaleString('fr-FR', { minimumFractionDigits: 0, maximumFractionDigits: 3 })} kg`;
  }
  const tons = kg / 1000;
  if (tons < 1000) {
    return `${tons.toLocaleString('fr-FR', { minimumFractionDigits: 0, maximumFractionDigits: 3 })} t`;
  }
  const kt = tons / 1000;
  return `${kt.toLocaleString('fr-FR', { minimumFractionDigits: 0, maximumFractionDigits: 3 })} kt`;
};

const handleJoinTribe = async (code: string) => {
  try {
    const res = await fetch('http://4.tcp.eu.ngrok.io:12316/api/tribe/join', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ invite: code, user_name: route.params.id })
    });
    if (!res.ok) {
      const err = await res.json();
      alert(err.message || 'Code invalide');
      return;
    }
    const data = await res.json();
    customVillage.value = data;
    if (data.team) {
      customVillage.value = data.team;
    }
  } catch (e) {
    console.error(e);
    alert('Impossible de contacter l\'API');
  }
}

onMounted(async () => {
  const storedName = sessionStorage.getItem('user_name');
  if (!storedName || storedName !== route.params.id) {
    alert('Accès refusé. Veuillez vous connecter.');
    window.location.href = '/';
    return;
  }

  try {
    const name = encodeURIComponent(route.params.id as string);
    const res = await fetch(`http://4.tcp.eu.ngrok.io:12316/api/user/name/${name}`);
    if (!res.ok) return;
    const data = await res.json();
    savedCO.value = data.saved_co || 0;
    if (data.team) {
      customVillage.value = data.team;
    }
  } catch (e) {
    console.error('Error fetching user info', e);
  }

  try {
    const res = await fetch('http://4.tcp.eu.ngrok.io:12316/missions');
    if (res.ok) {
      missions.value = await res.json();
    }
  } catch (e) {
    console.error('Error fetching missions', e);
  }
});

async function refreshUserAndTeam() {
  try {
    const name = encodeURIComponent(route.params.id as string);
    const res = await fetch(`http://4.tcp.eu.ngrok.io:12316/api/user/name/${name}`);
    if (!res.ok) return;
    const data = await res.json();
    savedCO.value = data.saved_co || 0;
    if (data.team) customVillage.value = data.team;
  } catch (e) {
    console.error('Error refreshing user', e);
  }
}

async function refreshMissions() {
  try {
    const res = await fetch('http://4.tcp.eu.ngrok.io:12316/missions');
    if (res.ok) missions.value = await res.json();
  } catch (e) {
    console.error('Error fetching missions', e);
  }
}

async function onMissionCompleted(payload: any) {
  if (payload.saved_co !== undefined) savedCO.value = payload.saved_co;
  if (payload.team) customVillage.value = payload.team;
  await refreshMissions();
}
</script>