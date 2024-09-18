const url = '/api';

export async function fetchIndices(){
  try {
    const response = await fetch(`${url}/get-indices`);
    const data = await response.json();
    console.log("index list: ", data);
    return data;
  } catch (error) {
    console.error('Error fetching index list:', error);
    return [];
  }
}

export async function loadFile(file: FormData) {
  try {
    console.log("file: ", file);
    const response = await fetch(`${url}/load-file`, {
      method: 'POST',
      body: file,
    });
    return response;
  } catch (error) {
    console.error('There was an error uploading the file:', error);
    return null;
  }
}

export async function fetchSettings() {
  try {
    const response = await fetch(`${url}/get-config`);
    return response.json();
  } catch (error) {
    console.error('Error fetching settings:', error);
  }
}

export async function updateSettings(settings: any) {
  try {
    const response = await fetch(`${url}/update-config`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(settings)
    });
    console.log(response.json);
  } catch (error) {
    console.error('Error updating settings:', error);
  }
}

export async function fetchRAG(query: string) {
  try {
    const response = await fetch(`${url}/query-rag`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ request: query }),
    });
    return response.json();
  } catch (error) {
    console.error('Error fetching RAG:', error);
    return null;
  }
}

export async function fetchGraph(index_name: string, list: number[]) {
  try {
    console.log("fetch graph request: ", index_name, list);
    const response = await fetch(`${url}/get-graph`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ index: index_name, values: list })
    });
    console.log("fetch graph response: ", response);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching graph:', error);
    return null;
  }
}

export async function deleteIndex(index: string) {
  try {
    const response = await fetch(`${url}/delete-index`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ request: index })
    });
    console.log(response.json);
  } catch (error) {
    console.error('Error deleting index:', error);
    return null;
  }
}
