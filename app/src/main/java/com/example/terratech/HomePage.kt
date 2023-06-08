package com.example.terratech

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.ImageButton
import android.widget.Toast
import com.google.firebase.database.FirebaseDatabase

class HomePage : AppCompatActivity() {

    private lateinit var database: FirebaseDatabase
    private var dataValue: String = "Deactivated" // Initial value

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)

        // Initialize Firebase Realtime Database
        database = FirebaseDatabase.getInstance()

        val updateButton = findViewById<ImageButton>(R.id.imageButton5)//pompa
        val button1 = findViewById<ImageButton>(R.id.imageButton3)//monitoring
        val button2 = findViewById<ImageButton>(R.id.imageButton4)//catatan_pompa
        val button3 = findViewById<ImageButton>(R.id.imageButton2)//Kendali_pompa
        val button4 = findViewById<ImageButton>(R.id.imageButton)//Pembelian_alat

        button1.setOnClickListener {
            // Navigate to Screen1
            val intent = Intent(this, MonitoringActivity::class.java)
            startActivity(intent)
        }

        button2.setOnClickListener {
            // Navigate to Screen2
//            val intent = Intent(this, Screen2::class.java)
//            startActivity(intent)
        }

        button3.setOnClickListener {
            // Navigate to Screen3
//            val intent = Intent(this, Screen3::class.java)
//            startActivity(intent)
        }

        button4.setOnClickListener {
            // Navigate to Screen4
            val intent = Intent(this, PurchaseToolsActivity::class.java)
            startActivity(intent)
        }

        updateButton.setOnClickListener {
            // Toggle data value between "Activated" and "Deactivated"
            if (dataValue == "Activated") {
                updateData("Deactivated")
            } else {
                updateData("Activated")
            }
        }
    }

    private fun updateData(newValue: String) {
        val databaseReference = database.reference.child("/relay_status")

        databaseReference.setValue(newValue)
            .addOnSuccessListener {
                // Data updated successfully
                Toast.makeText(this, "Data updated", Toast.LENGTH_SHORT).show()
                dataValue = newValue // Update the local data value
                updateButtonState() // Update the button text or appearance
            }
            .addOnFailureListener { exception ->
                // Failed to update data
                Toast.makeText(this, "Failed to update data: ${exception.message}", Toast.LENGTH_SHORT).show()
            }
    }

    private fun updateButtonState() {
        val updateButton = findViewById<ImageButton>(R.id.imageButton5)

        // Update button text or appearance based on the data value
        if (dataValue == "Activated") {
            updateButton.setImageResource(R.drawable.nyala)
        } else {
            updateButton.setImageResource(R.drawable.mati)
        }
    }
}
