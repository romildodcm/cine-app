<script>
let person_id = null;
let person_name = null;
let person = null;
let message = null;

async function getPersonById() {
    if (person_id === null){
        person = null;
        message = `${"ERRO: preencha o campo ID"}`;
        return;
    }

    const res = await fetch(
        `http://localhost:8000/artista/id/${person_id}`
    );
    const data = await res.json();
    if (res.ok) {
        person = data;
        message = null;        
    } else {
        person = null;
        message = `ID ${person_id} ${res.statusText}`;
    }
}

async function getPersonByName() {
    if (person_name === null){
        person = null;
        message = `${"ERRO: preencha o campo Nome"}`;
        return;
    }
    const res = await fetch(
        `http://localhost:8000/artista/name/${person_name}`
    );
    const data = await res.json();
    if (res.ok) {
        person = data;
        message = null;        
    } else {
        person = null;
        message = `Name ${person_name} ${res.statusText}`;
    }
}
</script>
<h1>Busca de Artistas</h1>
<!-- By id -->
<input bind:value={person_id} type="text" placeholder="person ID: 1100">
<button on:click={getPersonById}>
    find
</button>

<!-- By name -->
<input bind:value={person_name} type="text" placeholder="person name: Arnold">
<button on:click={getPersonByName}>
find
</button>

<div class="table">
    {#if person !== null}
        <p>ID: {person.id}</p>
        <p>Nome: {person.name}</p>
        <p>Popularidade: {person.popularity}</p>
        <img src="https://image.tmdb.org/t/p/w200/{person.profile_path}" alt={person.name} />
    {:else if message !== null}
        <p class='error'>{message}</p>
    {/if}
</div>

<style>
.error{
    color: #e35a5a;
}
.table{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    border: 1px solid #ccc;
    padding: 10px;
}
.table .desc{
    color: #646cff;
    grid-column: 1/4;
}
.person-img{
  display: block;
  margin-left: auto;
  margin-right: auto;
}
</style>