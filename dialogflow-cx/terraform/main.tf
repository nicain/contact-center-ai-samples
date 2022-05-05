# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

variable "build_uuid" {
  description = "Required uuid for a test build; links apply and destroy"
  type        = string
}

variable "project_id" {
  description = "Required uuid for a test build; links apply and destroy"
  type        = string
}

variable "access_token" {
  description = "Required uuid for a test build; links apply and destroy"
  type        = string
}

variable "webhook_function_name" {
  description = "Name of webhook function"
  type        = string
}

variable "webhook_function_entrypoint" {
  description = "Name of webhook function"
  type        = string
}

locals {
	root_dir = abspath("./")
  archive_path = abspath("./tmp/function.zip")
  region = "us-central1"
}

data "archive_file" "source" {
  type        = "zip"
  source_dir  = abspath("./webhook")
  output_path = local.archive_path
}

resource "google_storage_bucket" "bucket" {
  name     = "df-${var.build_uuid}"
  location = "US"
  project = var.project_id
}

provider "google" {
  project     = var.project_id
  region      = "us-central1"
  access_token = var.access_token
}

resource "google_storage_bucket_object" "archive" {
  name   = "index.zip"
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.source.output_path
  depends_on = [data.archive_file.source]
}

resource "google_cloudfunctions_function" "function" {
  project = var.project_id
  name        = var.webhook_function_name
  description = "Basic webhook"
  runtime     = "python39"
  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  trigger_http          = true
  timeout               = 60
  entry_point           = var.webhook_function_entrypoint
  region = "us-central1"
  depends_on = [google_storage_bucket_object.archive]
}

# IAM entry for a single user to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.function.project
  region         = google_cloudfunctions_function.function.region
  cloud_function = google_cloudfunctions_function.function.name
  role   = "roles/cloudfunctions.invoker"
  member = "serviceAccount:cf-envoker-${var.build_uuid}@${google_cloudfunctions_function.function.project}.iam.gserviceaccount.com"
  depends_on = [google_service_account.function_envoker]
}

resource "google_service_account" "function_envoker" {
  account_id   = "cf-envoker-${var.build_uuid}"
  display_name = "cf-envoker-${var.build_uuid}"
  project      = var.project_id
}

resource "google_project_iam_member" "df_admin" {
  project = var.project_id
  role    = "roles/dialogflow.admin"
  member  = "serviceAccount:df-admin-${var.build_uuid}@${google_cloudfunctions_function.function.project}.iam.gserviceaccount.com"
  depends_on = [google_service_account.dialogflow_admin]
}

resource "google_service_account" "dialogflow_admin" {
  account_id   = "df-admin-${var.build_uuid}"
  display_name = "df-admin-${var.build_uuid}"
  project      = var.project_id
}


