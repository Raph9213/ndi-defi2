<template>
  <nav class="bg-gray-200 sticky w-full z-20 top-0 start-0 border-b border-default shadow-xl mb-9">
    <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
      <a href="https://www.nuitdelinfo.com/inscription/equipes/515" class="flex items-center space-x-3 rtl:space-x-reverse">
          <img src="/peppers.webp" class="h-10" alt="Team's Logo" />
          <span class="self-center text-xl text-heading font-semibold whitespace-nowrap">Red Code Chili Peppers</span>
      </a>
      <button data-collapse-toggle="navbar-solid" type="button" class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-body rounded-base md:hidden hover:bg-neutral-secondary-soft hover:text-heading focus:outline-none focus:ring-2 focus:ring-neutral-tertiary" aria-controls="navbar-solid" aria-expanded="false">
          <span class="sr-only">Open main menu</span>
          <svg class="w-6 h-6" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-width="2" d="M5 7h14M5 12h14M5 17h14"/></svg>
      </button>
      <div class="hidden w-full md:block md:w-auto" id="navbar-solid">
  <ul class="font-medium flex flex-col p-4 md:p-0 mt-4 border border-default rounded-base bg-neutral-secondary-soft md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 md:bg-neutral-secondary-soft">
          <li>
            <a href="#" class="block py-2 px-3 text-gray-900 bg-brand rounded md:bg-transparent md:text-fg-brand md:p-0" aria-current="page">Accueil</a>
          </li>
          <li>
            <a href="#" class="block py-2 px-3 text-gray-900 rounded hover:bg-neutral-tertiary md:hover:bg-transparent md:border-0 md:hover:text-fg-brand md:p-0 md:dark:hover:bg-transparent">Dashboard</a>
          </li>
          <li>
            <a href="#" class="block py-2 px-3 text-gray-900 rounded hover:bg-neutral-tertiary md:hover:bg-transparent md:border-0 md:hover:text-fg-brand md:p-0 md:dark:hover:bg-transparent">Classement</a>
          </li>
          <li class="ml-2 flex items-center">
            <button @click="openPanel('register')" class="px-3 py-1 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">S'inscrire</button>
          </li>
          <li class="ml-2 flex items-center">
            <button @click="openPanel('login')" class="px-3 py-1 bg-white text-green-700 border border-green-600 rounded-lg hover:bg-green-50 transition-colors">Se connecter</button>
          </li>
        </ul>
      </div>
    </div>

    <div v-if="panelMode" class="register-panel">
      <h3 class="text-lg font-bold mb-2">{{ panelMode === 'register' ? "Créer un compte" : "Se connecter" }}</h3>
      <input v-model="name" v-if="panelMode === 'register'" type="text" placeholder="Nom" class="w-full mb-2 px-3 py-2 border rounded" />
      <input v-model="email" type="email" placeholder="Email" class="w-full mb-2 px-3 py-2 border rounded" />
      <input v-model="password" type="password" placeholder="Mot de passe" class="w-full mb-2 px-3 py-2 border rounded" />
      <div class="flex gap-2 mt-3">
        <button v-if="panelMode === 'register'" @click="registerUser" :disabled="loading" class="flex-1 bg-green-600 text-white py-2 rounded">{{ loading ? 'En cours...' : "S'inscrire" }}</button>
        <button v-else @click="loginUser" :disabled="loading" class="flex-1 bg-green-600 text-white py-2 rounded">{{ loading ? 'En cours...' : "Se connecter" }}</button>
        <button @click="closePanel" class="flex-1 bg-gray-200 py-2 rounded">Annuler</button>
      </div>
      <p class="text-sm text-red-600 mt-2">{{ message }}</p>
    </div>

  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const panelMode = ref<string | null>(null);
const name = ref('');
const email = ref('');
const password = ref('');
const loading = ref(false);
const message = ref('');

function openPanel(mode: string) { panelMode.value = mode; message.value = ''; }
function closePanel() { panelMode.value = null; name.value = ''; email.value = ''; password.value = ''; message.value = ''; }

async function registerUser() {
  if (!name.value || !email.value || !password.value) {
    message.value = 'Veuillez remplir tous les champs.';
    return;
  }
  loading.value = true;
  message.value = '';
  try {
    const res = await fetch('http://4.tcp.eu.ngrok.io:12316/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: name.value, email: email.value, password: password.value })
    });
    const data = await res.json();
    if (res.status === 201) {
      try { localStorage.setItem('ndi_token', data.token); localStorage.setItem('ndi_user', JSON.stringify(data.user)); } catch (e) {}
      window.location.href = `/users/${encodeURIComponent(data.user.name)}`;
    } else {
      message.value = data.message || 'Erreur lors de l\'inscription';
    }
  } catch (e) {
    console.error(e);
    message.value = 'Impossible de contacter le serveur.';
  } finally {
    loading.value = false;
  }
}

async function loginUser() {
  if (!email.value || !password.value) {
    message.value = 'Veuillez fournir email et mot de passe.';
    return;
  }
  loading.value = true;
  message.value = '';
  try {
    const res = await fetch('http://4.tcp.eu.ngrok.io:12316/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, password: password.value })
    });
    const data = await res.json();
    if (res.ok) {
      try { localStorage.setItem('ndi_token', data.token); localStorage.setItem('ndi_user', JSON.stringify(data.user)); } catch (e) {}
      window.location.href = `/users/${encodeURIComponent(data.user.name)}`;
    } else {
      message.value = data.message || 'Erreur de connexion';
    }
  } catch (e) {
    console.error(e);
    message.value = 'Impossible de contacter le serveur.';
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.register-panel {
  position: absolute;
  right: 1rem;
  top: 4rem;
  background: white;
  border: 1px solid rgba(0,0,0,0.06);
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 6px 18px rgba(0,0,0,0.08);
  width: 300px;
}
</style>
