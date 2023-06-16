package com.example.terratech

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.example.terratech.databinding.ActivityHomeBinding

class HomeActivity : AppCompatActivity() {
    private lateinit var binding: ActivityHomeBinding


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityHomeBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.shopButton.setOnClickListener {
            val intent = Intent(this, PurchaseToolsActivity::class.java)
            startActivity(intent)
        }

        binding.kondisiLahanButton.setOnClickListener {
            val intent = Intent(this, MonitoringActivity::class.java)
            startActivity(intent)
        }

//        binding.kondisiLahanButton.setOnClickListener {
//            val intent = Intent(this, KondisiLahanActivity::class.java)
//            startActivity(intent)
//        }
    }
}