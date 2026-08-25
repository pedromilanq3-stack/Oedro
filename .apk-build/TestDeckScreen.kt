package com.example.swipeautomator.ui

import androidx.compose.foundation.gestures.awaitEachGesture
import androidx.compose.foundation.gestures.awaitFirstDown
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.input.pointer.positionChange
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import kotlin.math.abs
import kotlin.math.roundToInt

@Composable
fun TestDeckScreen() {
    var index by remember { mutableIntStateOf(0) }
    var offsetX by remember { mutableFloatStateOf(0f) }
    val cards = remember { List(20) { "Sample card ${it + 1}" } }

    Column(
        modifier = Modifier.fillMaxSize().padding(20.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        Text("Internal Test Deck", style = MaterialTheme.typography.headlineSmall)
        Text("Start the controller, then return here. A qualifying horizontal swipe advances the card.")
        Text("Successful transitions: $index")

        Box(
            modifier = Modifier.fillMaxWidth().height(360.dp),
            contentAlignment = Alignment.Center,
        ) {
            Surface(
                tonalElevation = 4.dp,
                shape = RoundedCornerShape(24.dp),
                modifier = Modifier
                    .width(280.dp)
                    .height(320.dp)
                    .offset { IntOffset(offsetX.roundToInt(), 0) }
                    .pointerInput(index) {
                        awaitEachGesture {
                            val down = awaitFirstDown()
                            var totalX = 0f
                            var pressed = true
                            while (pressed) {
                                val event = awaitPointerEvent()
                                val change = event.changes.firstOrNull { it.id == down.id } ?: break
                                val delta = change.positionChange().x
                                totalX += delta
                                offsetX = totalX
                                change.consume()
                                pressed = change.pressed
                            }
                            val threshold = size.width * 0.25f
                            if (abs(totalX) >= threshold) {
                                offsetX = if (totalX > 0) size.width * 1.25f else -size.width * 1.25f
                                index = (index + 1).coerceAtMost(cards.size)
                            }
                            offsetX = 0f
                        }
                    },
            ) {
                Box(Modifier.fillMaxSize().padding(24.dp), contentAlignment = Alignment.Center) {
                    Text(cards.getOrElse(index) { "Deck complete" })
                }
            }
        }

        Button(onClick = {
            index = 0
            offsetX = 0f
        }) {
            Text("Reset deck")
        }
    }
}
