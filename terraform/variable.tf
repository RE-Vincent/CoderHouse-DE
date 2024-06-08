variable "credentials" {
  description = "projects's credentials"
  default     = "./keys/gcp-key.json"

}

variable "project" {
  description = "Project"
  default     = "project-etf-1001"
}

variable "region" {
  description = "Region"
  #Update the below to your desired region
  default = "us-central1"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default = "US"
}

variable "name" {
  description = "instance name"
  default     = "instance-airflow-etf-v1"

}

variable "machine_type" {
  description = "type of machine"
  default     = "e2-small"
}

variable "zone" {
  description = "zone configuration"
  default     = "us-central1-a"

}

variable "metada_script" {
  description = "config"
  default = "initscript_chef.sh"
}