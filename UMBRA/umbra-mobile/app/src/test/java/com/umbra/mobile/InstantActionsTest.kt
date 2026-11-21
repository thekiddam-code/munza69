package com.umbra.mobile
import kotlinx.serialization.json.*
import org.junit.Assert.*
import org.junit.Test
class InstantActionsTest {
    @Test fun quickChatUsesServerNamesAndSavedMessagesUseServerPayloads() {
        val pc=parsePcStatus(Json.parseToJsonElement("""{"quick":["Fresh server mapping"],"macros":["Configured macro"],"custom_messages":[{"label":"Rotate","text":"Rotating back","channel":"team"}]}""").jsonObject)
        val actions=instantActions(pc)
        val quick=actions.first {it.id.startsWith("quick:")}
        assertEquals("Fresh server mapping",quick.body.literal("name"));assertNull(quick.body["keys"])
        val message=actions.first {it.id.startsWith("message:")}
        assertEquals("Rotating back",message.body.literal("text"));assertEquals("team",message.body.literal("channel"))
        val changed=instantActions(pc.copy(messages=listOf(SavedMessage("Rotate","Different current message","team")))).first {it.id.startsWith("message:")}
        assertNotEquals(message.id,changed.id)
    }
    @Test fun malformedSavedMessagesAreRejectedWithoutTruncatingText() {
        val oversized="x".repeat(121)
        val payload=buildJsonObject {put("custom_messages",buildJsonArray {
            add(buildJsonObject {put("label","Invalid");put("text",oversized);put("channel","team")})
            add(buildJsonObject {put("label","Exact");put("text","Valid message");put("channel","match")})
        })}
        assertEquals(listOf(SavedMessage("Exact","Valid message","match")),parsePcStatus(payload).messages)
    }
}
