terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.29.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

data "google_compute_image" "ubuntu" {
  family  = "ubuntu-2004-lts"
  project = "ubuntu-os-cloud"
}

resource "google_compute_instance" "instance-t1" {
  boot_disk {
    auto_delete = true
    device_name = "instance-t1"

    initialize_params {
      image = data.google_compute_image.ubuntu.self_link
      size  = 15
      type  = "pd-balanced"
    }

    mode = "READ_WRITE"
  }

  can_ip_forward      = false
  deletion_protection = false
  enable_display      = false

  labels = {
    goog-ec-src = "vm_add-tf"
  }

  machine_type = "e2-small"
  name         = var.name
  zone         = var.zone

  network_interface {
    network = "default"
    access_config {} # Esto asigna una IP externa a la instancia
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }

  metadata = {
    vm = "tf"
  }

  metadata_startup_script = file(var.metada_script)
}