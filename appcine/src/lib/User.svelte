<script>
    import { onMount } from "svelte";
    let users = [];
    let user = {};
    let edit = false;

    onMount(async () => {
        const res = await fetch("http://localhost:8000/user/list");
        users = await res.json();
    });

    function handleSubmit(e) {
        e.preventDefault();
        if (edit) {
            updateUser();
        } else {
            createUser();
        }
    }

    async function createUser() {
        const res = await fetch("http://localhost:8000/user/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(user),
        });
        const newUser = await res.json();
        users = [...users, newUser];
        user = {};
    }

    async function updateUser() {
        const res = await fetch(
            `http://localhost:8000/user/update/${user.id}`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(user),
            }
        );

        // console.log("updateUser");
        // console.log(user);
        // console.log(res.json());

        user = {};
        const resList = await fetch("http://localhost:8000/user/list");
        users = await resList.json();
        edit = false;
    }

    async function deletaUser(id) {
        const res = await fetch(`http://localhost:8000/user/delete/${id}`, {
            method: "DELETE",
        });
        users = users.filter((u) => u.id !== id);
    }

    function ativaEdicao(id) {
        edit = true;
        user = users.find((u) => u.id === id);
    }
</script>

<div class="crud">
    <form on:submit|preventDefault={handleSubmit}>
        <input type="hidden" bind:value={user.id} />
        <div>
            <label>Name:</label>
            <input type="text" bind:value={user.name} />
        </div>
        <div>
            <label>Email:</label>
            <input type="email" bind:value={user.email} />
        </div>
        <div>
            <label>Password:</label>
            <input type="password" bind:value={user.password} />
        </div>
        <button type="submit">{edit ? "Update" : "Create"}</button>
    </form>
</div>

<table>
    <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {#each users as user}
            <tr>
                <td>{user.id}</td>
                <td>{user.name}</td>
                <td>{user.email}</td>
                <td>
                    <button on:click={() => ativaEdicao(user.id)}>Edit</button>
                    <button on:click={() => deletaUser(user.id)}>Delete</button>
                </td>
            </tr>
        {/each}
    </tbody>
</table>

