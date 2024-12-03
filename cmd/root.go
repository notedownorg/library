// Copyright 2024 Notedown Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package cmd

import (
	"fmt"
	"os"
	"strings"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var (
	Version    string
	CommitHash string
)

var rootCmd = &cobra.Command{
	Use:     "library",
	Short:   "A tool to store the media you consume to your notes",
	Version: version(),
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	cobra.OnInitialize(initConfig)
}

type config struct {
	home string
	root string
}

func loadConfig() config {
	cfg := config{}
	cfg.root = viper.GetString("dir")
	if cfg.root == "" {
		fmt.Println("Please set NOTEDOWN_DIR environment variable to the root of your Notedown workspace")
		os.Exit(1)
	}

	home, err := os.UserHomeDir()
	if err != nil {
		fmt.Println("error getting user home directory:", err)
		os.Exit(1)
	}
	cfg.home = home

	return cfg
}

// initConfig reads in config file and ENV variables if set.
func initConfig() {
	viper.SetEnvPrefix("notedown")
	viper.BindEnv("dir")
	viper.AutomaticEnv() // read in environment variables that match
}

func version() string {
	var b strings.Builder

	if Version == "" {
		b.WriteString("dev")
	} else {
		b.WriteString(Version)
	}

	if CommitHash != "" {
		b.WriteString("-")
		b.WriteString(CommitHash)
	}

	return b.String()
}