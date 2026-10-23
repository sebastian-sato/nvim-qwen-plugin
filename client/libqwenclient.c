#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <curl/curl.h>
#include <lua.h>
#include <lauxlib.h>

#define BUFFER_SIZE 64000

// Internal error codes
#define SUCCESS 0
#define CURL_INIT_FAIL 1
#define PAYLOAD_TOO_BIG 2
#define FAILED_TO_CONNECT 3

struct MemoryStruct {
    char* memory;
    size_t size;
};

static size_t
WriteMemoryCallback(void* contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct MemoryStruct *mem = (struct MemoryStruct*)userp;

    char *ptr = realloc(mem->memory, mem->size + realsize + 1);

    if (!ptr) {
        printf("Not enough memory (realloc returned NULL)\n");
        return 0;
    }

    mem->memory = ptr;
    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->memory[mem->size] = 0;

    return realsize;
}

bool make_request_string(char* buffer, const char* query, const char* payload) {
	int current_null_index = 0;
	int query_size = strlen(query) + 1;
	int payload_size = strlen(payload) + 1;

	const int STATIC_SIZE = 16;

	int total_size = query_size + payload_size + STATIC_SIZE + 50; // +50 cuz you never know

	if (total_size > BUFFER_SIZE) {
		return false;
	}

	sprintf(buffer + current_null_index, "query="); 
	current_null_index = 6;
	snprintf(buffer + current_null_index, query_size, "%s", query); 
	current_null_index += query_size - 1; 
	sprintf(buffer + current_null_index, "&payload=");
	current_null_index += 9;
	snprintf(buffer + current_null_index, payload_size, "%s", payload);

	return true;
}

int request(char* buffer, const char* payload, const char* query, const char* address) { // Returns error status
    CURL *curl;
    CURLcode result;

    struct MemoryStruct chunk;
    chunk.memory = malloc(1);
    chunk.size = 0;

    curl = curl_easy_init();
    if (curl == NULL) {
        fprintf(stderr, "CURL initialization failed\n");
        return CURL_INIT_FAIL;
    }

    //curl_easy_setopt(curl, CURLOPT_VERBOSE, 1);

    curl_easy_setopt(curl, CURLOPT_URL, address);

    char input_buffer[BUFFER_SIZE];
    bool make_request_string_success = make_request_string(input_buffer, query, payload);

    if (!make_request_string_success) {
        return PAYLOAD_TOO_BIG;
    }

    curl_easy_setopt(curl, CURLOPT_POST, 1);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, input_buffer);
    curl_easy_setopt(curl, CURLOPT_PORT, 8000);

    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);

    result = curl_easy_perform(curl);

    if (result != CURLE_OK) {
        fprintf(stderr, "Error: %s\n", curl_easy_strerror(result));
        free(chunk.memory);  // Free allocated memory before returning
        return FAILED_TO_CONNECT;
    }

    int index = 0;
    while (1) {
	buffer[index] = chunk.memory[index];
	if (chunk.memory[index] == 0) {
		break;
	}
	index++;
    }

    free(chunk.memory);  // Free allocated memory
    curl_easy_cleanup(curl);

    return SUCCESS; 
}

static int l_process(lua_State *L)
{
    const char* payload = luaL_checkstring(L, 1);
    const char* query = luaL_checkstring(L, 2);
    const char* address = luaL_checkstring(L, 3);

    char buffer[BUFFER_SIZE];
    int status = request(buffer, payload, query, address);

    const char* result = buffer;

    switch (status) {
        case SUCCESS:
            lua_pushstring(L, result);
            break;
        case CURL_INIT_FAIL:
            lua_pushstring(L, "E: internal failure");
            break;
        case FAILED_TO_CONNECT:
            lua_pushstring(L, "E: failed to connect to server");
            break;
        case PAYLOAD_TOO_BIG:
            lua_pushstring(L, "E: payload too big");
            break;
        default:
            lua_pushstring(L, "E: invalid status encountered, something is very wrong.");
            break;
    }

    return 1;
}

static const luaL_Reg mylib[] = {
    {"process", l_process},
    {NULL, NULL}
};

int luaopen_libqwenclient(lua_State *L)
{
    luaL_newlib(L, mylib);
    return 1;
}
