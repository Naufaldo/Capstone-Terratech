package com.example.terratech

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.example.terratech.databinding.ActivityHomeBinding
import com.example.terratech.databinding.ActivityMonitoringBinding

class MonitoringActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMonitoringBinding
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMonitoringBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.monitoringTanahCard.setOnClickListener {
            val intent = Intent(this, KondisiLahanActivity::class.java)
            startActivity(intent)
        }
    }
}